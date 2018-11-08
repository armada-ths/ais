from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

from fair.models import Fair
from companies.models import Company
from people.models import DietaryRestriction

from .models import Participant
from .forms import ParticipantForm, DietaryRestrictionsTableForm


@permission_required('unirel.base')
def admin(request, year):
	fair = get_object_or_404(Fair, year = year)
	participants = Participant.objects.filter(fair = fair)
	
	count_banquet = 0
	count_sleep = 0
	count_lunch = 0
	
	for participant in participants:
		if participant.addon_banquet: count_banquet += 1
		if participant.addon_sleep: count_sleep += 1
		if participant.addon_lunch: count_lunch += 1
	
	return render(request, 'unirel/admin.html', {
		'fair': fair,
		'participants': participants,
		'count_banquet': count_banquet,
		'count_sleep': count_sleep,
		'count_lunch': count_lunch
	})


@permission_required('unirel.base')
def admin_dietary_restrictions(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	participants_all = Participant.objects.filter(fair = fair)
	
	form = DietaryRestrictionsTableForm(request.POST or None)
	
	if request.POST and form.is_valid():
		if form.cleaned_data['addon_sleep']: participants_all = participants_all.exclude(addon_sleep = False)
		if form.cleaned_data['addon_lunch']: participants_all = participants_all.exclude(addon_lunch = False)
		if form.cleaned_data['addon_banquet']: participants_all = participants_all.exclude(addon_banquet = False)
	
	dietary_restrictions_all = {}
	
	for participant in participants_all:
		for dietary_restriction in participant.dietary_restrictions.all():
			if dietary_restriction in dietary_restrictions_all: dietary_restrictions_all[dietary_restriction].append(participant)
			else: dietary_restrictions_all[dietary_restriction] = [participant]
	
	participants = []
	
	for participant in participants_all:
		l = [(participant in dietary_restrictions_all[x]) for x in dietary_restrictions_all]
		
		participants.append({
			'participant': participant,
			'dietary_restrictions': l
		})
	
	return render(request, 'unirel/admin_dietary_restrictions.html', {
		'fair': fair,
		'form': form,
		'participants': participants,
		'dietary_restrictions': [{'name': x, 'count': len(dietary_restrictions_all[x])} for x in dietary_restrictions_all],
	})


@permission_required('unirel.base')
def admin_participant(request, year, participant_pk = None):
	fair = get_object_or_404(Fair, year = year)
	participant = get_object_or_404(Participant, pk = participant_pk, fair = fair) if participant_pk is not None else None
	
	return render(request, 'unirel/admin_participant.html', {
		'fair': fair,
		'participant': participant,
		'url': request.build_absolute_uri(reverse('unirel_register', args = [participant.token]))
	})


@permission_required('unirel.base')
def admin_participant_delete(request, year, participant_pk):
	fair = get_object_or_404(Fair, year = year)
	participant = get_object_or_404(Participant, pk = participant_pk, fair = fair)
	
	participant.delete()
	
	return redirect('unirel_admin', fair.year)


@permission_required('unirel.base')
def admin_participant_form(request, year, participant_pk = None):
	fair = get_object_or_404(Fair, year = year)
	participant = get_object_or_404(Participant, pk = participant_pk, fair = fair) if participant_pk is not None else None
	
	form = ParticipantForm(request.POST or None, instance = participant)
	
	if request.POST and form.is_valid():
		form.instance.fair = fair
		participant = form.save()
		return redirect('unirel_admin_participant', fair.year, participant.pk)
	
	return render(request, 'unirel/admin_participant_form.html', {
		'fair': fair,
		'form': form
	})


def register(request, token):
	participant = get_object_or_404(Participant, token = token)
	
	form = ParticipantForm(request.POST or None, instance = participant)
	
	form.fields['company'].queryset = Company.objects.filter(pk = participant.company.pk)
	form.fields['company'].disabled = True
	form.fields['company'].hidden = True
	form.fields['name'].disabled = True
	form.fields['email_address'].disabled = True
	form.fields['phone_number'].required = True
	
	if request.POST and form.is_valid():
		form.save()
		form = None
	
	return render(request, 'unirel/register.html', {
		'participant': participant,
		'form': form
	})
