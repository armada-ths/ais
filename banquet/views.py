import datetime, json
import requests as r
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms import modelform_factory

from django import forms
from django.views.generic import CreateView, ListView, TemplateView, RedirectView, UpdateView

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from people.models import Language, Profile

from .models import Banquet, Participant, Invitation
from .forms import InternalParticipantForm, ExternalParticipantForm, SendInvitationForm


#External Invite
class ExternalInviteRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        Check if object exists by token
        if it does send to updateview
        """
        invitation = Invitation.objects.get(token=self.kwargs["token"])
        if invitation.participant:
            return reverse_lazy('external_invite_update', kwargs=self.kwargs, current_app='banquet')
        else:
            return reverse_lazy('external_invite_create', kwargs=self.kwargs, current_app='banquet')

class ExternalInviteUpdateView(UpdateView):
    """
    UpdateView for external
    """
    model = Participant
    form_class = ExternalParticipantForm
    template_name = 'banquet/invite.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Get invitation object
        """
        self.invitation = get_object_or_404(Invitation, token=self.kwargs["token"])
        self.participant = self.invitation.participant
        self.year = self.invitation.banquet.fair.year
        return super(ExternalInviteUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Set partipant as what we are updating
        """
        return self.participant

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('external_invite_thankyou', kwargs=self.kwargs, current_app='banquet')

    def get_context_data(self, **kwargs):
        """
        Adding year
        """
        context = super(ExternalInviteUpdateView, self).get_context_data(**kwargs)
        context['year'] = self.year
        return context

class ExternalInviteCreateView(CreateView):
    """
    Invite view for students and invitees (excl. companies)
    """
    form_class = ExternalParticipantForm
    template_name = 'banquet/invite.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if valid token
        """
        token = self.kwargs["token"]

        if not Invitation.objects.filter(token=token).exists():
            return HttpResponseForbidden()
        self.invitation = get_object_or_404(Invitation, token = token)

        if(self.invitation.participant):
            return redirect(reverse_lazy('external_invite_update', kwargs=self.kwargs, current_app='banquet'))
        else:
            self.year = self.invitation.banquet.fair.year
            return super(ExternalInviteCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('external_invite_thankyou', kwargs=self.kwargs, current_app='banquet')

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ExternalInviteCreateView, self).get_initial()
        # kinda ugly, prob better to modify model
        initial['name'] = self.invitation.name
        initial['email_address'] = self.invitation.email_address

        return initial

    def get_context_data(self, **kwargs):
        """
        Adding year
        """
        context = super(ExternalInviteCreateView, self).get_context_data(**kwargs)
        context['year'] = self.year
        return context

    def form_valid(self, form):
        form.instance.banquet = self.invitation.banquet
        form.instance.email_address = self.invitation.email_address
        self.object = form.save()
        self.invitation.participant = self.object
        self.invitation.save()
        return super(ExternalInviteCreateView, self).form_valid(form)

class GeneralMixin(object):
    """
    Shared functions of Banquet pages
    We will always need to add use some parameters e.g. year banquet
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Adding year, fair as parameters
        """
        self.user = self.request.user
        self.year = self.kwargs['year']
        self.fair = get_object_or_404(Fair, year=self.year)
        # TODO: Allow for multiple banquets in a year
        self.banquet = Banquet.objects.get(fair=self.fair)

        return super(GeneralMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adding fair,year to our context for consistency with other templates
        """
        context = super(GeneralMixin, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['fair'] = self.fair
        return context

class InternalInviteRedirectView(GeneralMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if Invitation.objects.filter(banquet=self.banquet, participant__user=self.request.user).exists():
            return reverse_lazy('internal_invite_update', kwargs=self.kwargs, current_app='banquet')
        else:
            return reverse_lazy('internal_invite_create', kwargs=self.kwargs, current_app='banquet')

class InternalInviteUpdateView(GeneralMixin, UpdateView):
    """
    Invite view for already registered students
    """
    model = Participant
    form_class = InternalParticipantForm
    template_name = 'banquet/internal_invite.html'

    def get_object(self):
        """
        Which object are we updating
        """
        return get_object_or_404(Participant, banquet=self.banquet, user=self.request.user)

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('invite_list', kwargs=self.kwargs, current_app='banquet')

class InternalInviteCreateView(GeneralMixin, CreateView):
    """
    Invite view for already registered students
    """
    form_class = InternalParticipantForm
    template_name = 'banquet/internal_invite.html'

    def dispatch(self, request, *args, **kwargs):
        """
        @overites GeneralMixin >:(
        For security
        Redirects to updateview if object exists
        """
        self.user = self.request.user
        self.year = self.kwargs['year']
        self.fair = get_object_or_404(Fair, year=self.year)
        # TODO: Allow for multiple banquets in a year
        self.banquet = Banquet.objects.get(fair=self.fair)
        if Invitation.objects.filter(banquet=self.banquet, participant__user=self.request.user).exists():
            return redirect(reverse_lazy('internal_invite_update', kwargs=self.kwargs, current_app='banquet'))
        return super(InternalInviteCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(InternalInviteCreateView, self).get_initial()
        user_profile = Profile.objects.get(user=self.user)
        # kinda ugly, prob better to modify model
        initial['name'] = self.user.get_full_name()
        initial['email_address'] = self.user.email
        initial['phone_number'] = user_profile.phone_number

        return initial

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('invite_list', kwargs=self.kwargs, current_app='banquet')

    def form_valid(self, form):
        """
        Modified so form doesn't need to have user, banquet
        Also creates an invitation
        """
        form.instance.user = self.user
        form.instance.banquet = self.banquet
        # participant
        self.object = form.save()
        invitation = Invitation.create(
            banquet=self.banquet,
            participant=self.object,
            name=form.instance.name,
            email_address=form.instance.email_address,
            reason="Armada Member",
            price=0
        )
        invitation.save()
        return super(InternalInviteCreateView, self).form_valid(form)

class SendInviteCreateView(GeneralMixin, CreateView):
    """
    Banquet group can set who to invite
    """
    form_class = SendInvitationForm
    template_name = 'banquet/send_invite.html'

    def get_success_url(self):
        return reverse_lazy('invite_list', kwargs=self.kwargs, current_app='banquet')

    def form_valid(self, form):
        form.instance.banquet = self.banquet
        return super(SendInviteCreateView, self).form_valid(form)

def export_invitations(request, year):
    """
    Exports invitations of banquet
    so we can send out mail(not through ais)
    """
    # here's why I prefer class based views
    # I already did this before >:(
    fair = get_object_or_404(Fair, year=year)
    #TODO: handle multiple banquets in a year
    banquet = Banquet.objects.get(fair=fair)
    invitations = Invitation.objects.filter(banquet=banquet)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="banquet_invitations.csv"'

    writer = csv.writer(response, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(['name','email_address','invite_link'])
    for invitation in invitations:
        token = invitation.token
        #if external
        if invitation.user is None:
            link = request.build_absolute_uri(
                reverse(
                    'external_invite_redirect',
                    kwargs={"token":token},
                )
            )
        else:
            link = request.build_absolute_uri(
                reverse(
                    'internal_invite_redirect',
                    kwargs={"year":year},
                )
            )
        writer.writerow([invitation.name, invitation.email_address, link])
        token = None
    return response

class SentInvitationsListView(GeneralMixin, ListView):
    """
    List who's been invited
    """
    template_name = 'banquet/invite_list.html'

    def get_queryset(self):
        return Invitation.objects.filter(banquet=self.banquet)

    def get_context_data(self, **kwargs):
        """
        Adding fair,year to our context for consistency with other templates
        """
        context = super(SentInvitationsListView, self).get_context_data(**kwargs)
        ##remove invitation in template if already exists
        context['participant'] = Participant.objects.filter(user = self.request.user).first()
        return context

class ParticipantsListView(GeneralMixin, ListView):
    """
    List who's been invited
    """
    template_name = 'banquet/participant_list.html'

    def get_queryset(self):
        return Participant.objects.filter(banquet=self.banquet)

class ThankYouView(TemplateView):
    template_name='banquet/thank_you.html'
