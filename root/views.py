from recruitment.models import RecruitmentPeriod, Role
from events.models import Event
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from exhibitors.models import BanquetteAttendant
from django.urls import reverse
from people.models import Profile
from fair.models import Fair

def login_redirect(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]

    if request.user.is_authenticated():
        return redirect('home', 2017)

    return render(request, 'login.html', {
        'next': next,
    })

def index(request, year):
    fair = get_object_or_404(Fair, year=year)
    if request.user.is_authenticated():
        return render(request, "root/home.html", {
            "recruitment": {
                'recruitment_periods': RecruitmentPeriod.objects.filter(fair=fair).order_by('-start_date'),
                'roles': [{'parent_role': role,
                           'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]}
                          for
                          role in Role.objects.filter(parent_role=None)],
            },
            "events": Event.objects.filter(fair=fair).order_by("-event_start"),
            "is_attending_banquette": BanquetteAttendant.objects.filter(fair=fair, user=request.user).exists(),
            "fair": fair
        })

    return render(request, 'login.html', {
        'next': next,
        'fair': fair
    })


def banquette_signup(request, year, template_name='exhibitors/related_object_form.html'):
    fair = get_object_or_404(Fair, year=year)
    if request.user.is_authenticated():
        instance = BanquetteAttendant.objects.filter(fair=fair, user=request.user).first()
        FormFactory = modelform_factory(BanquetteAttendant, exclude=('user', 'exhibitor', 'first_name', 'last_name', 'email', 'student_ticket', 'table_name', 'seat_number', 'ignore_from_placement'))
        form = FormFactory(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.first_name = request.user.first_name
            instance.last_name = request.user.last_name
            instance.email = request.user.email
            instance.save()
            return redirect('home', fair.year)
        delete_url = reverse(banquette_signup_delete)
        return render(request, template_name,
                      {'form': form, 'exhibitor': None, 'instance': instance, 'model_name': 'Banquet',
                       'delete_url': delete_url, 'fair': fair})

    return render(request, 'login.html', {'next': next, 'fair': fair})

def banquet_attendants(request, year, template_name='banquet/banquet_attendants.html'):
    fair = get_object_or_404(Fair, year=year)
    if request.user.is_authenticated():
        banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
        return render(request, template_name, {
            'banquet_attendants': banquet_attendants,
            'fair': fair
        })

    return render(request, 'login.html', {'next': next, 'fair': fair})


def banquette_signup_delete(request, year):
    fair = get_object_or_404(Fair, year=year)
    if request.POST:
        instance = get_object_or_404(BanquetteAttendant, user=request.user, fair=fair)
        instance.delete()
    return redirect('/')
