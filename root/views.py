from recruitment.models import RecruitmentPeriod, Role
from events.models import Event
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from exhibitors.models import BanquetteAttendant
from django.urls import reverse


def index(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]
    print(next)

    if request.user.is_authenticated():
        data = {}

        data["recruitment"] = {
            'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
            'roles': [{'parent_role': role,
                       'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]}
                      for
                      role in Role.objects.filter(parent_role=None)],
        }

        data["events"] = Event.objects.all().order_by("event_start")
        data["is_attending_banquette"] = BanquetteAttendant.objects.filter(user=request.user).exists()

        return render(request, "root/home.html", data)

    return render(request, 'login.html', {'next': next})


def banquette_signup(request, template_name='exhibitors/related_object_form.html'):
    if request.user.is_authenticated():
        instance = BanquetteAttendant.objects.filter(user=request.user).first()
        FormFactory = modelform_factory(BanquetteAttendant, exclude=('user', 'exhibitor','first_name', 'last_name', 'email'))
        form = FormFactory(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.first_name = request.user.first_name
            instance.last_name = request.user.last_name
            instance.email = request.user.email
            instance.save()
            return redirect('/')
        delete_url = reverse(banquette_signup_delete)
        return render(request, template_name,
                      {'form': form, 'exhibitor': None, 'instance': instance, 'model_name': 'Banquet',
                       'delete_url': delete_url})

    return render(request, 'login.html', {'next': next})


def banquette_signup_delete(request):
    if request.POST:
        instance = get_object_or_404(BanquetteAttendant, user=request.user)
        instance.delete()
    return redirect('/')
