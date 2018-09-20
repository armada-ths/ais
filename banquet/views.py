import datetime, json
import requests as r

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
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
from django.views.generic import CreateView

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from people.models import Language, Profile

from .models import Banquet, DietaryPreference, Participant, Invitation
from .forms import InternalParticipantForm, ExternalParticipantForm

class InviteMixin(object):
    """
    Shared functions of invite pages
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Adding year, fair as parameters
        """
        self.user = self.request.user
        self.year = self.kwargs['year']
        self.fair = get_object_or_404(Fair, year=self.year)
        return super(InviteMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adding fair,year to our context for consistency with other templates
        """
        context = super(InviteMixin, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['fair'] = self.fair
        return context

    def form_valid(self, form):
        """
        Modified so form doesn't need to have banquet and user,
        instead sent with the form on succesfull form
        """
        form.instance.banquet = Banquet.objects.get(fair=self.fair)
        form.instance.user = self.user

        return super(InviteMixin, self).form_valid(form)

class InternalInviteView(InviteMixin, CreateView):
    """
    Invite view for students and invitees (excl. companies)
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

class ExternalInviteView(InviteMixin, CreateView):
    """
    Invite view for students and invitees (excl. companies)
    """
    # Form: Participant
    form_class = ExternalParticipantForm
    template_name = 'banquet/invite.html'
    success_url = '/'
# class ExternalInviteView(InviteMixin, CreateView):
#     """
#     Invite view for students and invitees (excl. companies)
#     """
#     # Form: Participant
#     form_class = ParticipantForm
#     template_name = 'banquet/invite.html'
#     success_url = '/'
#
#
#     def get_context_data(self, **kwargs):
#         """
#         Adding fair,year to our context for consistency with other templates
#         """
#         context = super(InviteView, self).get_context_data(**kwargs)
#         context['year'] = self.year
#         context['fair'] = self.fair
#         return context
#
#     def get_form(self, form_class):
#         form = super(InviteView, self).get_form(form_class)
#         if not user.is_anonymous():
#             form.fields['name'].widget.attrs['readonly'] = True
#             form.fields['email_address'].widget.attrs['readonly'] = True
#             form.fields['phone_number'].widget.attrs['readonly'] = True
#         return form
#
#     def get_initial(self):
#         """
#         Returns the initial data to use for forms on this view.
#         """
#         initial = super(InviteView, self).get_initial()
#         if not user.is_anonymous():
#             user_profile = Profile.objects.get(user=user)
#             # kinda ugly, prob better to modify model
#             initial['name'] = user.get_full_name()
#             initial['email_address'] = user.email
#             initial['phone_number'] = user_profile.phone_number
#
#         return initial

# class InviteView(InviteMixin, CreateView):
#     """
#     Invite view for students and invitees (excl. companies)
#     """
#     # Form: Participant
#     form_class = ParticipantForm
#     template_name = 'banquet/invite.html'
#     success_url = '/'
#
#
#     def get_context_data(self, **kwargs):
#         """
#         Adding fair,year to our context for consistency with other templates
#         """
#         context = super(InviteView, self).get_context_data(**kwargs)
#         context['year'] = self.year
#         context['fair'] = self.fair
#         return context
#
#     def get_form(self, form_class):
#         form = super(InviteView, self).get_form(form_class)
#         if not user.is_anonymous():
#             form.fields['name'].widget.attrs['readonly'] = True
#             form.fields['email_address'].widget.attrs['readonly'] = True
#             form.fields['phone_number'].widget.attrs['readonly'] = True
#         return form
#
#     def get_initial(self):
#         """
#         Returns the initial data to use for forms on this view.
#         """
#         initial = super(InviteView, self).get_initial()
#         if not user.is_anonymous():
#             user_profile = Profile.objects.get(user=user)
#             # kinda ugly, prob better to modify model
#             initial['name'] = user.get_full_name()
#             initial['email_address'] = user.email
#             initial['phone_number'] = user_profile.phone_number
#
#         return initial
