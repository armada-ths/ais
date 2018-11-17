import datetime, json, csv, stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.mail import send_mail
from django.views.generic import CreateView, ListView, TemplateView, RedirectView, UpdateView

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from people.models import Language, Profile
from accounting.models import Order
from recruitment.models import OrganizationGroup, RecruitmentApplication

from .models import Banquet, Participant, InvitationGroup, Invitation, AfterPartyTicket, Table, Seat
from .forms import InternalParticipantForm, ExternalParticipantForm, SendInvitationForm, InvitationForm, InvitationSearchForm, ParticipantForm, ParticipantAdminForm, AfterPartyTicketForm


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

def dashboard(request, year):
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
def manage(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	count_ordered = 0
	
	for order in Order.objects.filter(product = banquet.product):
		count_ordered += order.quantity
	
	return render(request, 'banquet/manage.html', {
		'fair': fair,
		'banquet': banquet,
		'count_going': Invitation.objects.filter(banquet = banquet).exclude(participant = None).count(),
		'count_not_going': Invitation.objects.filter(banquet = banquet, denied = True).count(),
		'count_invitations': Invitation.objects.filter(banquet = banquet).count(),
		'count_pending': Invitation.objects.filter(banquet = banquet, denied = False, participant = None).count(),
		'count_ordered': count_ordered,
		'count_created': Participant.objects.filter(banquet = banquet).exclude(company = None).count(),
		'count_participants': Participant.objects.filter(banquet = banquet).count()
	})


@permission_required('banquet.base')
def manage_invitations(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	invitations = []
	
	for invitation in Invitation.objects.select_related('user').select_related('group').filter(banquet = banquet):
		invitations.append({
			'pk': invitation.pk,
			'group': invitation.group,
			'name': invitation.user.get_full_name() if invitation.user is not None else invitation.name,
			'email_address': invitation.user.email if invitation.user is not None else invitation.email_address,
			'reason': invitation.reason,
			'status': invitation.status,
			'price': invitation.price,
			'status': invitation.status,
			'deadline_smart': invitation.deadline_smart
		})
	
	form = InvitationSearchForm(request.POST or None)
	
	form.fields['groups'].queryset = InvitationGroup.objects.filter(banquet = banquet)
	
	has_filtering = request.POST and form.is_valid()
	
	invitations_modified = []
	
	for invitation in invitations:
		if has_filtering:
			if len(form.cleaned_data['groups']) > 0:
				found = False
				
				for group in form.cleaned_data['groups']:
					if invitation['group'] == group:
						found = True
						break
				
				if not found: continue
			
			if len(form.cleaned_data['statuses']) > 0:
				found = False
				
				for status in form.cleaned_data['statuses']:
					if invitation['status'] == status:
						found = True
						break
				
				if not found: continue
		
		invitations_modified.append(invitation)
	
	
	return render(request, 'banquet/manage_invitations.html', {
		'fair': fair,
		'banquet': banquet,
		'invitiations': invitations_modified,
		'form': form
	})


@permission_required('banquet.base')
def manage_invitation(request, year, banquet_pk, invitation_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	invitation = get_object_or_404(Invitation, banquet = banquet, pk = invitation_pk)
	
	return render(request, 'banquet/manage_invitation.html', {
		'fair': fair,
		'banquet': banquet,
		'invitation': invitation
	})


@permission_required('banquet.base')
def manage_invitation_form(request, year, banquet_pk, invitation_pk = None):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	invitation = get_object_or_404(Invitation, banquet = banquet, pk = invitation_pk) if invitation_pk is not None else None
	
	form = InvitationForm(request.POST or None, instance = invitation)
	
	users = []
	users_flat = []
	
	for organization_group in OrganizationGroup.objects.filter(fair = fair):
		this_users_flat = [application.user for application in RecruitmentApplication.objects.select_related('user').filter(delegated_role__organization_group = organization_group, status = 'accepted', recruitment_period__fair = fair).order_by('user__first_name', 'user__last_name')]
		users_flat += this_users_flat
		users.append([organization_group.name, [(user.pk, user.get_full_name()) for user in this_users_flat]])
	
	if invitation is not None and invitation.user is not None and invitation.user not in users_flat:
		users = [(invitation.user.pk, invitation.user.get_full_name())] + users
	
	users = [('', '---------')] + users
	
	form.fields['user'].choices = users
	
	groups = [(group.pk, group.name + ' (' + ('deadline ' + str(group.deadline) if group.deadline is not None else 'no deadline') + ')') for group in InvitationGroup.objects.filter(banquet = banquet)]
	
	form.fields['group'].choices = groups
	
	if invitation is not None and invitation.participant is not None:
		form.fields['price'].disabled = True
		form.fields['price'].help_text = 'The price cannot be changed as the invitation has already been accepted.'
	
	if request.POST and form.is_valid():
		form.instance.banquet = banquet
		invitation = form.save()
		
		if invitation.participant is not None and invitation.participant.user is None and invitation.participant.company is None:
			invitation.participant.name = invitation.name
			invitation.participant.email_address = invitation.email_address
		
		return redirect('banquet_manage_invitation', fair.year, banquet.pk, invitation.pk)
	
	return render(request, 'banquet/manage_invitation_form.html', {
		'fair': fair,
		'banquet': banquet,
		'invitation': invitation,
		'form': form
	})


@permission_required('banquet.base')
def manage_participants(request, year, banquet_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	
	participants = [{
		'pk': participant.pk,
		'company': participant.company,
		'user': participant.user,
		'name': participant.user.get_full_name() if participant.user else participant.name,
		'email_address': participant.user.email if participant.user else participant.email_address,
		'alcohol': participant.alcohol,
		'seat': participant.seat
	} for participant in Participant.objects.select_related('seat').select_related('seat__table').filter(banquet = banquet)]
	
	return render(request, 'banquet/manage_participants.html', {
		'fair': fair,
		'banquet': banquet,
		'participants': participants
	})


@permission_required('banquet.base')
def manage_participant_form(request, year, banquet_pk, participant_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	participant = get_object_or_404(Participant, banquet = banquet, pk = participant_pk)
	
	form = ParticipantAdminForm(request.POST or None, instance = participant)
	
	seats_taken = [p.seat for p in Participant.objects.select_related('seat').exclude(seat = None)]
	
	seats = []
	
	for table in Table.objects.filter(banquet = banquet):
		table_seats = []
		
		for table_seat in Seat.objects.filter(table = table):
			if table_seat not in seats_taken: table_seats.append((table_seat.pk, table_seat.name))
		
		seats.append([table, table_seats])
	
	form.fields['seat'].choices = [('', '---------')] + seats
	
	users = []
	all_users = []
	
	for organization_group in OrganizationGroup.objects.filter(fair = fair):
		this_users_flat = [application.user for application in RecruitmentApplication.objects.select_related('user').filter(delegated_role__organization_group = organization_group, status = 'accepted', recruitment_period__fair = fair).order_by('user__first_name', 'user__last_name')]
		all_users += this_users_flat
		users.append([organization_group.name, [(user.pk, user.get_full_name()) for user in this_users_flat]])
	
	if participant is not None and participant.user is not None and participant.user not in all_users: users = [(participant.user.pk, participant.user.get_full_name())] + users
	
	form.fields['user'].choices = [('', '---------')] + users
	
	if request.POST and form.is_valid():
		participant = form.save()
		
		invitation = Invitation.objects.filter(participant = participant).first()
		
		if invitation is not None:
			invitation.user = participant.user
			invitation.name = participant.name
			invitation.email_address = participant.email_address
			invitation.save()
		
		return redirect('banquet_manage_participants', fair.year, banquet.pk)
	
	return render(request, 'banquet/manage_participant_form.html', {
		'fair': fair,
		'banquet': banquet,
		'form': form,
		'participant': participant
	})


@permission_required('banquet.base')
def manage_participant_remove(request, year, banquet_pk, participant_pk):
	fair = get_object_or_404(Fair, year = year)
	banquet = get_object_or_404(Banquet, fair = fair, pk = banquet_pk)
	participant = get_object_or_404(Participant, banquet = banquet, pk = participant_pk)
	
	participant.delete()
	
	return redirect('banquet_manage_participants', fair.year, banquet.pk)



def invitation(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	invitation = get_object_or_404(Invitation, banquet__fair = fair, token = token, user = request.user)
	
	participant = invitation.participant if invitation.participant is not None else Participant(banquet = invitation.banquet, user = request.user)
	
	participant.name = request.user.get_full_name()
	participant.email_address = request.user.email
	
	form = ParticipantForm(request.POST or None, instance = participant)
	
	form.fields['phone_number'].required = True
	
	if invitation.banquet.caption_phone_number is not None: form.fields['phone_number'].help_text = invitation.banquet.caption_phone_number
	if invitation.banquet.caption_dietary_restrictions is not None: form.fields['dietary_restrictions'].help_text = invitation.banquet.caption_dietary_restrictions
	
	can_edit = invitation.deadline_smart is None or invitation.deadline_smart >= datetime.datetime.now().date()
	
	if can_edit:
		if request.POST and form.is_valid() and can_edit:
			if invitation.participant is None and invitation.price > 0:
				stripe.api_key = settings.STRIPE_SECRET
				
				charge = stripe.Charge.create(
					amount = invitation.price * 100, # Stripe wants the price in ören
					currency = 'SEK',
					description = 'Banquet invitation token ' + str(invitation.token),
					source = request.POST['stripeToken']
				)
			
			else:
				charge = None
			
			form.instance.name = None
			form.instance.email_address = None
			invitation.participant = form.save()
			invitation.save()
			
			if charge is not None:
				invitation.participant.charge_stripe = charge['id']
				invitation.participant.save()
			
			form = None
	
	else:
		form = None
	
	return render(request, 'banquet/invitation_internal.html', {
		'fair': fair,
		'invitation': invitation,
		'form': form,
		'charge': invitation.price > 0 and invitation.participant is None,
		'stripe_publishable': settings.STRIPE_PUBLISHABLE,
		'stripe_amount': invitation.price * 100,
		'can_edit': can_edit
	})


def invitation_no(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	invitation = get_object_or_404(Invitation, banquet__fair = fair, token = token, user = request.user)
	
	if invitation.deadline_smart is not None and datetime.datetime.now().date() > invitation.deadline_smart: return HttpResponseForbidden()
	
	if invitation.participant is not None:
		if invitation.participant.charge_stripe is not None:
			stripe.api_key = settings.STRIPE_SECRET
			refund = stripe.Refund.create(charge = invitation.participant.charge_stripe)
		
		invitation.participant.delete()
		invitation.participant = None
	
	invitation.denied = True
	invitation.save()
	
	return redirect('banquet_invitation', fair.year, invitation.token)


def invitation_maybe(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	invitation = get_object_or_404(Invitation, banquet__fair = fair, token = token, user = request.user)
	
	if invitation.deadline_smart is not None and datetime.datetime.now().date() > invitation.deadline_smart: return HttpResponseForbidden()
	
	invitation.denied = False
	invitation.save()
	
	return redirect('banquet_invitation', fair.year, invitation.token)


def external_invitation(request, token):
	invitation = get_object_or_404(Invitation, token = token, user = None)
	
	participant = invitation.participant if invitation.participant is not None else Participant(banquet = invitation.banquet, user = None)
	
	participant.name = invitation.name
	participant.email_address = invitation.email_address
	
	form = ParticipantForm(request.POST or None, instance = participant)
	
	form.fields['phone_number'].required = True
	
	if invitation.banquet.caption_phone_number is not None: form.fields['phone_number'].help_text = invitation.banquet.caption_phone_number
	if invitation.banquet.caption_dietary_restrictions is not None: form.fields['dietary_restrictions'].help_text = invitation.banquet.caption_dietary_restrictions
	
	can_edit = invitation.deadline_smart is None or invitation.deadline_smart >= datetime.datetime.now().date()
	
	if can_edit:
		if request.POST and form.is_valid():
			if invitation.participant is None and invitation.price > 0:
				stripe.api_key = settings.STRIPE_SECRET
				
				charge = stripe.Charge.create(
					amount = invitation.price * 100, # Stripe wants the price in ören
					currency = 'SEK',
					description = 'Banquet invitation token ' + invitation.token,
					source = request.POST['stripeToken']
				)
			
			else:
				charge = None
			
			form.instance.name = invitation.name
			form.instance.email_address = invitation.email_address
			invitation.participant = form.save()
			invitation.save()
			
			if charge is not None:
				invitation.participant.charge_stripe = charge['id']
				invitation.participant.save()
			
			form = None
	
	else:
		form = None
	
	return render(request, 'banquet/invitation_external.html', {
		'invitation': invitation,
		'form': form,
		'charge': invitation.price > 0 and invitation.participant is None,
		'stripe_publishable': settings.STRIPE_PUBLISHABLE,
		'stripe_amount': invitation.price * 100,
		'can_edit': can_edit
	})


def external_invitation_no(request, token):
	invitation = get_object_or_404(Invitation, token = token, user = None)
	
	if invitation.deadline_smart is not None and datetime.datetime.now().date() > invitation.deadline_smart: return HttpResponseForbidden()
	
	if invitation.participant is not None:
		if invitation.participant.charge_stripe is not None:
			stripe.api_key = settings.STRIPE_SECRET
			refund = stripe.Refund.create(charge = invitation.participant.charge_stripe)
		
		invitation.participant.delete()
		invitation.participant = None
	
	invitation.denied = True
	invitation.save()
	
	return redirect('banquet_external_invitation', invitation.token)


def external_invitation_maybe(request, token):
	invitation = get_object_or_404(Invitation, token = token, user = None)
	
	if invitation.deadline_smart is not None and datetime.datetime.now().date() > invitation.deadline_smart: return HttpResponseForbidden()
	
	invitation.denied = False
	invitation.save()
	
	return redirect('banquet_external_invitation', invitation.token)


def external_banquet_afterparty(request, token = None):
	fair = get_object_or_404(Fair, current = True)
	ticket = get_object_or_404(AfterPartyTicket, token = token) if token is not None else None
	
	amount = 75
	form = None
	
	if ticket is None:
		form = AfterPartyTicketForm(request.POST or None)
	
		if request.POST and form.is_valid():
			ticket = form.save()
			return redirect('banquet_external_afterparty_token', ticket.token)
	
	elif request.POST and ticket.paid_price is None:
		stripe.api_key = settings.STRIPE_SECRET
		
		charge = stripe.Charge.create(
			amount = amount * 100, # Stripe wants the price in ören
			currency = 'SEK',
			description = 'After party ticket ' + str(ticket.token),
			source = request.POST['stripeToken']
		)
		
		ticket.charge_stripe = charge['id']
		ticket.paid_timestamp = datetime.datetime.now()
		ticket.paid_price = amount
		ticket.save()
		
		send_mail(
			'Your ticket for the After Party',
			'Hello ' + ticket.name + '! Welcome to the After Party at the Grand Banquet of THS Armada. Your ticket is available here:\nhttps://ais.armada.nu/banquet/afterparty/' + str(ticket.token) + '\n\nTime and date: November 20, 22:00\nLocation: Münchenbryggeriet\n\nWelcome!',
			'info@armada.nu',
			[ticket.email_address],
			fail_silently = True,
		)
	
	return render(request, 'banquet/afterparty.html', {
		'fair': fair,
		'form': form,
		'stripe_publishable': settings.STRIPE_PUBLISHABLE,
		'stripe_amount': amount * 100,
		'amount': amount,
		'ticket': ticket
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
