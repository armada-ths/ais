from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from companies.models import CompanyContact
from events.models import Event
from fair.models import Fair
from recruitment.models import RecruitmentPeriod, Role


def login_redirect(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]

    if request.user.is_authenticated():
        contact = CompanyContact.objects.filter(user=request.user).first()

        if contact is not None:
            return redirect('anmalan:choose_company')

        return redirect('home', 2018)

    return render(request, 'login.html', {'next': next})


def index(request, year=None):
    fair = Fair.objects.filter(current=True).first()
    if fair is None:
        fair = get_object_or_404(Fair, year=year)
    if request.user.is_authenticated():

        if request.user.has_perm('events.base'):
            events = Event.objects.filter(fair=fair).annotate(num_participants=Count('participant'))
        else:
            events = Event.objects.filter(fair=fair, published=True)

        return render(request, "root/home.html", {
            "recruitment": {
                'recruitment_periods': RecruitmentPeriod.objects.filter(fair=fair).order_by('-start_date'),
                'roles': [{'parent_role': role,
                           'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]}
                          for
                          role in Role.objects.filter(parent_role=None)],
            },
            'events': events,
            "fair": fair
        })

    return render(request, 'login.html', {
        'next': next,
        'fair': fair
    })
