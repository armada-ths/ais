from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from companies.models import CompanyContact
from events.models import Event
from recruitment.models import RecruitmentApplication, RecruitmentPeriod, Role
from people.models import DietaryRestriction
from exhibitors.models import Exhibitor

from .forms import LunchTicketForm, LunchTicketSearchForm
from .models import Fair, FairDay, LunchTicket, OrganizationGroup


def login_redirect(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]

    if request.user.is_authenticated():
        contact = CompanyContact.objects.filter(user=request.user).first()

        if contact is not None:
            return redirect('anmalan:choose_company')

        return redirect('fair:home', 2018)

    return render(request, 'login.html', {'next': next})


def index(request, year = None):
	fair = Fair.objects.filter(current = True).first()
	if fair is None:
		fair = get_object_or_404(Fair, year=year)
		
	if not request.user.is_authenticated():
		return render(request, 'login.html', {
			'next': next,
			'fair': fair
		})
		
	if request.user.has_perm('events.base'): events = Event.objects.filter(fair = fair).annotate(num_participants = Count('participant'))
	else: events = Event.objects.filter(fair = fair, published = True)

	return render(request, 'fair/home.html', {
		'recruitment': {
			'recruitment_periods': RecruitmentPeriod.objects.filter(fair=fair).order_by('-start_date'),
			'roles': [{
				'parent_role': role,
				'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]
			} for role in Role.objects.filter(parent_role=None)],
		},
		'events': events,
		'fair': fair
	})


def lunchtickets(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	form = LunchTicketSearchForm(request.POST or None)
	
	form.fields['days'].queryset = FairDay.objects.filter(fair = fair)
	
	if request.POST and form.is_valid():
		lunchtickets = LunchTicket.objects.select_related('user').select_related('company').select_related('day').select_related('time').prefetch_related('dietary_restrictions').filter(fair = fair)
		lunchtickets_filtered = []
		
		for lunchticket in lunchtickets:
			if len(form.cleaned_data['statuses']) > 0:
				found = False
				
				for s in form.cleaned_data['statuses']:
					if s == 'USED' and lunchticket.used:
						found = True
						break
					
					if s == 'NOT_USED' and not lunchticket.used:
						found = True
						break
				
				if not found: continue
			
			if len(form.cleaned_data['types']) > 0:
				found = False
				
				for t in form.cleaned_data['types']:
					if t == 'STUDENT' and lunchticket.company is None:
						found = True
						break
					
					if t == 'COMPANY' and lunchticket.company is not None:
						found = True
						break
				
				if not found: continue
			
			if len(form.cleaned_data['days']) > 0:
				found = False
				
				for d in form.cleaned_data['days']:
					if lunchticket.day == d:
						found = True
						break
				
				if not found: continue
			
			lunchtickets_filtered.append({
				't': lunchticket,
				'drl': []
			})
		
		dietary_restrictions_all = {}
		
		if form.cleaned_data['include_dietary_restrictions']:
			for lunchticket in lunchtickets_filtered:
				for dietary_restriction in lunchticket['t'].dietary_restrictions.all():
					if dietary_restriction in dietary_restrictions_all: dietary_restrictions_all[dietary_restriction] += 1
					else: dietary_restrictions_all[dietary_restriction] = 1
			
			for lunchticket in lunchtickets_filtered:
				lunchticket['drl'] = [True if dietary_restriction in lunchticket['t'].dietary_restrictions.all() else False for dietary_restriction in dietary_restrictions_all]
	
	else:
		lunchtickets_filtered = []
		dietary_restrictions_all = {}
	
	return render(request, 'fair/lunchtickets.html', {
		'fair': fair,
		'my_lunchtickets': LunchTicket.objects.filter(fair = fair, user = request.user),
		'form': form,
		'has_searched': request.POST and form.is_valid(),
		'lunchtickets': lunchtickets_filtered,
		'dietary_restrictions': [{'name': x, 'count': dietary_restrictions_all[x]} for x in dietary_restrictions_all]
	})


def lunchticket(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	lunch_ticket = get_object_or_404(LunchTicket, fair = fair, token = token)
	
	if request.user != lunch_ticket.user and not request.user.has_perm('fair.lunchtickets'): return HttpResponseForbidden()
	
	if request.user.has_perm('fair.lunchtickets'):
		form = LunchTicketForm(request.POST or None, instance = lunch_ticket)
		
		if request.POST and form.is_valid(): form.save()
	
	else:
		form = None
	
	return render(request, 'fair/lunchticket.html', {
		'fair': fair,
		'lunch_ticket': lunch_ticket,
		'form': form
	})


@permission_required('fair.lunchtickets')
def lunchticket_remove(request, year, token):
	fair = get_object_or_404(Fair, year = year)
	lunch_ticket = get_object_or_404(LunchTicket, fair = fair, token = token)
	
	lunch_ticket.delete()
	
	return redirect('fair:lunchtickets', fair.year)


@permission_required('fair.lunchtickets')
def lunchticket_create(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	form = LunchTicketForm(request.POST or None, initial = {'fair': fair})
	
	form.fields['company'].choices = [('', '---------')] + [(exhibitor.company.pk, exhibitor.company.name) for exhibitor in Exhibitor.objects.select_related('company').filter(fair = fair).order_by('company')]
	
	users = []
	
	for organization_group in OrganizationGroup.objects.filter(fair = fair):
		this_users_flat = [application.user for application in RecruitmentApplication.objects.select_related('user').filter(delegated_role__organization_group = organization_group, status = 'accepted', recruitment_period__fair = fair).order_by('user__first_name', 'user__last_name')]
		users.append([organization_group.name, [(user.pk, user.get_full_name()) for user in this_users_flat]])
	
	form.fields['user'].choices = [('', '---------')] + users
	
	if request.POST and form.is_valid():
		form.instance.fair = fair
		lunch_ticket = form.save()
		return redirect('fair:lunchticket', fair.year, lunch_ticket.token)
	
	return render(request, 'fair/lunchticket_create.html', {
		'fair': fair,
		'form': form
	})
