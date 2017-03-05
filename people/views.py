from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from recruitment.models import RecruitmentApplication
from .models import Profile
from django.utils import timezone
from django import forms
from django.core.exceptions import PermissionDenied

from recruitment.views import set_image_key_from_request

from django.forms import ModelForm
from django.contrib.auth.decorators import permission_required
from fair.models import Fair

@permission_required('people.view_people', raise_exception=True)
def list_people(request, year):
    fair = get_object_or_404(Fair, year=year)
    users = User.objects.filter(is_superuser=False)
    return TemplateResponse(request, 'people_list.html', {'users': users, 'fair': fair})


def view_person(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk=pk)

    if (request.user == user) or request.user.has_perm('people.view_people'):
        profile = Profile.objects.get_or_create(user=user)[0]

        application = RecruitmentApplication.objects.filter(user=user, status='accepted').first()
        return TemplateResponse(request, 'view_person.html', {
            'person': profile,
            'role': application.delegated_role if application else "",
            'fair': fair,
        })
    else:
        raise PermissionDenied


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', 'image')

        widgets = {
            "registration_year": forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)]),
            "birth_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }
        labels= {'birth_date': 'Birth date (format: 2016-12-24)'}


def edit_person(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk=pk)
    if not request.user == user:
        raise PermissionDenied

    profile = Profile.objects.get_or_create(user=user)[0]

    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        set_image_key_from_request(request, profile, 'image', 'profile')
        return redirect('view_person', fair.year, user.pk)

    application = RecruitmentApplication.objects.filter(user=user, status='accepted').first()
    return TemplateResponse(request, 'edit_person.html', {
        'person': profile,
        'role': application.delegated_role if application else "",
        'form': form,
        'fair': fair,
    })

