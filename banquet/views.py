import datetime, json
import requests as r

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
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
from django.views.generic import CreateView, ListView

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from people.models import Language, Profile
from django.urls import reverse_lazy

from .models import Banquet, Participant, Invitation
from .forms import InternalParticipantForm, ExternalParticipantForm, SendInvitationForm

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

class InviteCreateFormMixin(GeneralMixin,object):
    """
    Shared form_valid for invite createViews
    """
    def form_valid(self, form):
        """
        Modified so form doesn't need to have banquet and user,
        instead sent with the form on succesfull form
        """
        form.instance.user = self.user
        form.instance.banquet = self.banquet

        return super(InviteCreateFormMixin, self).form_valid(form)

class InternalInviteView(InviteCreateFormMixin, CreateView):
    """
    Invite view for already registered students
    """
    # Form: Participant
    form_class = InternalParticipantForm
    template_name = 'banquet/invite.html'
    success_url = '/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(InternalInviteView, self).get_initial()
        user_profile = Profile.objects.get(user=self.user)
        # kinda ugly, prob better to modify model
        initial['name'] = self.user.get_full_name()
        initial['email_address'] = self.user.email
        initial['phone_number'] = user_profile.phone_number

        return initial

class ExternalInviteView(InviteCreateFormMixin, CreateView):
    """
    Invite view for students and invitees (excl. companies)
    """
    # Form: Participant
    form_class = ExternalParticipantForm
    template_name = 'banquet/invite.html'
    success_url = '/'

class SendInviteCreateView(InviteCreateFormMixin, CreateView):
    """
    Banquet group can set who to invite
    """
    form_class = SendInvitationForm
    template_name = 'banquet/send_invite.html'
    success_url = reverse_lazy('invite_list')

class SentInvitationsListView(GeneralMixin, ListView):
    """
    List who's been invited
    """
    template_name = 'banquet/invite_list.html'

    def get_queryset(self):
        return Invitation.objects.filter(banquet=self.banquet)
