import json

from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from banquet.models import Participant, Banquet
from companies.models import CompanyContact
from events.models import Event
from fair import serializers
from recruitment.models import RecruitmentApplication
from recruitment.models import RecruitmentPeriod, Role

from .forms import LunchTicketForm, LunchTicketSearchForm
from .models import Fair, LunchTicket, LunchTicketSend
from .models import FairDay, OrganizationGroup


from fair.selectors import get_fair, get_lunch_tickets, get_serialized_lunch_tickets, get_lunch_ticket, get_banquet_particiapnt
from fair.services import send_lunch_ticket, create_lunch_ticket_form


def login_redirect(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]

    if request.user.is_authenticated():
        contact = CompanyContact.objects.filter(user=request.user).first()
        year = timezone.now().year

        if contact is not None:
            return redirect('anmalan:choose_company')

        return redirect('fair:home', year)

    return render(request, 'login.html', {'next': next})


def index(request, year=None):
    fair = Fair.objects.filter(current=True).first()
    if fair is None:
        fair = get_object_or_404(Fair, year=year)

    if not request.user.is_authenticated():
        return render(request, 'login.html', {
            'next': next,
            'fair': fair
        })

    if request.user.has_perm('events.base'):
        events = Event.objects.filter(fair=fair).annotate(num_participants=Count('participant'))
    else:
        events = Event.objects.filter(fair=fair, published=True)

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


@permission_required('fair.lunchtickets')
def lunchtickets(request, year):
    fair = get_fair(year=year)
    form = LunchTicketSearchForm(request.POST or None)

    form.fields['days'].queryset = FairDay.objects.filter(fair=fair)

    if request.POST and form.is_valid():
        lunchtickets = LunchTicket.objects.select_related('user').select_related('company').select_related('day').select_related(
            'time').prefetch_related('dietary_restrictions').filter(fair=fair)
        lunchtickets_filtered = []

        for lunchticket in lunchtickets:
            if len(form.cleaned_data['used_statuses']) > 0:
                found = False

                for s in form.cleaned_data['used_statuses']:
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

            if len(form.cleaned_data['sent_statuses']) > 0:
                found = False

                for t in form.cleaned_data['sent_statuses']:
                    if t == 'SENT' and lunchticket.sent:
                        found = True
                        break

                    if t == 'NOT_SENT' and not lunchticket.sent:
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
                    if dietary_restriction in dietary_restrictions_all:
                        dietary_restrictions_all[dietary_restriction] += 1
                    else:
                        dietary_restrictions_all[dietary_restriction] = 1

            for lunchticket in lunchtickets_filtered:
                lunchticket['drl'] = [True if dietary_restriction in lunchticket['t'].dietary_restrictions.all() else False for
                                      dietary_restriction in dietary_restrictions_all]

    else:
        lunchtickets_filtered = []
        dietary_restrictions_all = {}

    return render(request, 'fair/lunchtickets.html', {
        'fair': fair,
        'my_lunchtickets': get_lunch_tickets(fair=fair, user=request.user),
        'form': form,
        'has_searched': request.POST and form.is_valid(),
        'lunchtickets': lunchtickets_filtered,
        'dietary_restrictions': [{'name': x, 'count': dietary_restrictions_all[x]} for x in dietary_restrictions_all]
    })


@permission_required('fair.lunchtickets')
def lunchticket(request, year, token):
    fair = get_fair(year=year)
    lunch_ticket = get_lunch_ticket(token=token)

    if request.user != lunch_ticket.user and not request.user.has_perm('fair.lunchtickets'):
        return HttpResponseForbidden()

    if request.user.has_perm('fair.lunchtickets'):
        form = LunchTicketForm(request.POST or None, instance=lunch_ticket)

        if request.POST and form.is_valid(): 
            form.save()

    else:
        form = None

    return render(request, 'fair/lunchticket.html', {
        'fair': fair,
        'lunch_ticket': lunch_ticket,
        'form': form,
        'sends': LunchTicketSend.objects.filter(lunch_ticket = lunch_ticket)
    })


@permission_required('fair.lunchtickets')
def lunchticket_remove(request, year, token):
    fair = get_fair(year=year)
    lunch_ticket = get_lunch_ticket(token=token)
    lunch_ticket.delete()

    return redirect('fair:lunchtickets', fair.year)


@permission_required('fair.lunchtickets')
def lunchticket_send(request, year, token):
    fair = get_fair(year=year)
    lunch_ticket = get_lunch_ticket(token=token)
    lunch_ticket_token = send_lunch_ticket(lunch_ticket=lunch_ticket, user=request.user)

    return redirect('fair:lunchticket', fair.year, lunch_ticket_token)


@permission_required('fair.lunchtickets')
def lunchticket_create(request, year):
    fair = get_fair(year=year)
    form = create_lunch_ticket_form(fair=fair)
    
    if request.POST and form.is_valid():
        form.instance.fair = fair
        lunch_ticket = form.save()
        return redirect('fair:lunchticket', fair.year, lunch_ticket.token)

    return render(request, 'fair/lunchticket_create.html', {
        'fair': fair,
        'form': form
    })


@permission_required('fair.lunchtickets')
def lunchtickets_check_in(request, year):
    return render(request, 'fair/lunch_ticket_check_in.html', {
        'react_props': json.dumps({})
    })

def lunchticket_display(request, token):
    return render(request, 'fair/lunchticket_display.html', {
        'lunch_ticket': get_lunch_ticket(token=token)
    })


def tickets(request, year):
    fair = get_fair(year=year)
    react_props = {
        'lunch_tickets': get_serialized_lunch_tickets(fair=fair, user=request.user),
        'banquet_participant': get_banquet_particiapnt(fair=fair, user=request.user),
    }

    return render(request, 'fair/tickets.html', {
        'fair': fair,
        'react_props': json.dumps(react_props)
    })
