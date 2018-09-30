from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.decorators import permission_required

from fair.models import Fair
from recruitment.models import RecruitmentApplication

from .models import Profile
from .forms import ProfileForm


def view_person(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk=pk)

    if (request.user == user) or request.user.has_perm('people.base'):
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            profile = Profile.objects.create(user = user, no_dietary_restrictions = False)

        application = RecruitmentApplication.objects.filter(
                user=user,
                status='accepted',
                recruitment_period__fair__current=True
            ).last()
        return TemplateResponse(request, 'view_person.html', {
            'person': profile,
            'role': application.delegated_role if application else "",
            'fair': fair,
        })
    else:
        raise PermissionDenied


def edit_person(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk=pk)
    if not request.user == user:
        raise PermissionDenied

    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile = Profile.objects.create(user=user)

    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('view_person', fair.year, user.pk)

    application = RecruitmentApplication.objects.filter(user=user, status='accepted').first()
    return TemplateResponse(request, 'edit_person.html', {
        'person': profile,
        'role': application.delegated_role if application else "",
        'form': form,
        'fair': fair,
    })

