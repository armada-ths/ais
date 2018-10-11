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
from .forms import InternalParticipantForm, ExternalParticipantForm, SendInvitationForm, InvitationForm


#External Invite
class ExternalInviteRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        Check if object exists by token
        if it does send to updateview
        """
        invitation = get_object_or_404(Invitation, token=self.kwargs["token"])
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
        return reverse_lazy('external_invite_thankyou', kwargs={"year":self.kwargs["year"]}, current_app='banquet')

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
        invitation = get_object_or_404(Invitation, token = self.kwargs["token"], user = self.request.user)
        #actual redirect
        if invitation.participant:
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
        return get_object_or_404(Invitation, token = self.kwargs["token"], user = self.request.user)

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('invite_list', kwargs={"year" : self.kwargs["year"]}, current_app='banquet')

class InternalInviteCreateView(GeneralMixin, CreateView):
    """
    Invite view for already registered students
    """
    form_class = InternalParticipantForm
    template_name = 'banquet/internal_invite.html'

    def dispatch(self, request, *args, **kwargs):
        """
        For security
        Redirects to updateview if object exists
        """
        self.user = self.request.user
        self.year = self.kwargs['year']
        self.token = self.kwargs['token']
        self.invitation = get_object_or_404(Invitation, token = self.token, user=self.request.user)
        if self.invitation.participant:
            return redirect(reverse_lazy('internal_invite_update', kwargs=self.kwargs, current_app='banquet'))
        self.banquet = self.invitation.banquet
        self.user_profile = Profile.objects.get(user=self.user)
        return super(InternalInviteCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(InternalInviteCreateView, self).get_initial()
        # kinda ugly, prob better to modify model
        initial['name'] = self.user.get_full_name()
        initial['email_address'] = self.user.email
        initial['phone_number'] = self.user_profile.phone_number

        return initial

    def get_success_url(self):
        """
        We have some kwargs e.g. year that we need to send
        """
        return reverse_lazy('invite_list', kwargs={"year":self.kwargs["year"]}, current_app='banquet')

    def form_valid(self, form):
        """
        Modified so form doesn't need to have user, banquet
        Also creates an invitation
        """
        form.instance.banquet = self.invitation.banquet
        form.instance.user = self.user
        self.object = form.save()
        self.invitation.participant = self.object
        self.invitation.save()
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
        if form.instance.user:
            form.instance.name = form.instance.user.get_full_name()
            form.instance.email_address = form.instance.user.email

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
                    kwargs={"year":year,"token":token}
                )
            )
        writer.writerow([invitation.name, invitation.email_address, link])
        token = None
    return response

def banquet_dashboard(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	banquets = []
	
	for banquet in Banquet.objects.filter(fair = fair):
		banquets.append({
			'pk': banquet.pk,
			'name': banquet.name,
			'date': banquet.date,
			'location': banquet.location,
			'count_going': Participant.objects.filter(banquet = banquet).count(),
			'count_not_going': Invitation.objects.filter(banquet = banquet, denied = True).count(),
			'count_pending': Invitation.objects.filter(banquet = banquet, participant = None).exclude(denied = True).count()
		})
	
	return render(request, 'banquet/dashboard.html', {
		'fair': fair,
		'invitiations': Invitation.objects.filter(user = request.user),
		'banquets': banquets
	})


@permission_required('banquet.base')
def banquet_manage(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	return render(request, 'banquet/manage.html', {
		'fair': fair,
		'banquet': banquet
	})


@permission_required('banquet.base')
def banquet_manage_invitations(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	invitations = []
	
	for invitation in Invitation.objects.filter(banquet = banquet):
		if invitation.participant is not None: status = 'GOING'
		elif invitation.denied: status = 'NOT_GOING'
		else: status = 'PENDING'
		
		invitations.append({
			'pk': invitation.pk,
			'name': invitation.user.get_full_name() if invitation.user is not None else invitation.name,
			'email_address': invitation.user.email if invitation.user is not None else invitation.email_address,
			'reason': invitation.reason,
			'status': status,
			'price': invitation.price
		})
	
	return render(request, 'banquet/manage_invitations.html', {
		'fair': fair,
		'banquet': banquet,
		'invitiations': invitations
	})


@permission_required('banquet.base')
def banquet_manage_invitation(request, year, banquet_pk, invitation_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	invitation = get_object_or_404(Invitation, banquet = banquet, pk = invitation_pk)
	
	return render(request, 'banquet/manage_invitation.html', {
		'fair': fair,
		'banquet': banquet,
		'invitation': invitation
	})


@permission_required('banquet.base')
def banquet_manage_invitation_form(request, year, banquet_pk, invitation_pk = None):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	invitation = get_object_or_404(Invitation, banquet = banquet, pk = invitation_pk) if invitation_pk is not None else None
	
	form = SendInvitationForm(request.POST or None, instance = invitation)
	
	if request.POST and form.is_valid():
		form.instance.banquet = banquet
		invitation = form.save()
		return redirect('banquet_manage_invitation', fair.year, banquet.pk, invitation.pk)
	
	return render(request, 'banquet/manage_invitation_form.html', {
		'fair': fair,
		'banquet': banquet,
		'invitation': invitation,
		'form': form
	})


@permission_required('banquet.base')
def banquet_manage_participants(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	return render(request, 'banquet/manage_participants.html', {
		'fair': fair,
		'banquet': banquet,
		'participants': Participant.objects.filter(banquet = banquet)
	})


def banquet_invitation(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	invitation = get_object_or_404(Invitation, banquet__fair = fair, token = token, user = request.user)
	
	participant = invitation.participant if invitation.participant is not None else Participant(banquet = invitation.banquet, user = request.user)
	
	participant.name = request.user.get_full_name()
	participant.email_address = request.user.email
	
	form = InvitationForm(request.POST or None, instance = participant)
	
	if invitation.banquet.caption_phone_number is not None: form.fields['phone_number'].help_text = invitation.banquet.caption_phone_number
	if invitation.banquet.caption_dietary_restrictions is not None: form.fields['dietary_restrictions'].help_text = invitation.banquet.caption_dietary_restrictions
	
	if request.POST and form.is_valid():
		form.instance.name = None
		form.instance.email_address = None
		invitation.participant = form.save()
		invitation.save()
		form = None
	
	return render(request, 'banquet/invitation_internal.html', {
		'fair': fair,
		'invitation': invitation,
		'form': form
	})


class ParticipantsListView(GeneralMixin, ListView):
    """
    List who's been invited
    """
    template_name = 'banquet/participant_list.html'

    def get_queryset(self):
        return Participant.objects.filter(banquet=self.banquet)

class ThankYouView(TemplateView):
    template_name='banquet/thank_you.html'
