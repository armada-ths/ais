from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
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
    return TemplateResponse(request, 'view_person.html', {'person': profile})
    
