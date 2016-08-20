from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from recruitment.models import RecruitmentApplication
from .models import Profile

from recruitment.views import set_image_key_from_request

from django.forms import ModelForm
# Create your views here.

@login_required(login_url='/login/')
def list_people(request):
    return TemplateResponse(request, 'people_list.html', {'users': User.objects.all()})

@login_required(login_url='/login/')
def view_person(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile = Profile.objects.create(user=user)

    application = RecruitmentApplication.objects.filter(user=user, status='accepted').first()
    return TemplateResponse(request, 'view_person.html', {
        'person': profile,
        'role': application.delegated_role if application else ""
    })


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', 'image')


@login_required(login_url='/login/')
def edit_person(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile = Profile.objects.create(user=user)

    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        set_image_key_from_request(request, profile, 'image', 'profile')

    application = RecruitmentApplication.objects.filter(user=user, status='accepted').first()
    return TemplateResponse(request, 'edit_person.html', {
        'person': profile,
        'role': application.delegated_role if application else "",
        'form': form
    })

