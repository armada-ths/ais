from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

from fair.models import Fair
from companies.models import Company

from .models import Participant
from .forms import ParticipantForm


@permission_required('unirel.base')
def admin(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	return render(request, 'unirel/admin.html', {
		'fair': fair,
		'participants': Participant.objects.filter(fair = fair)
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
	
	if request.POST and form.is_valid():
		form.save()
		form = None
	
	return render(request, 'unirel/register.html', {
		'participant': participant,
		'form': form
	})
