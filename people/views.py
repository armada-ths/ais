from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def list_people(request):
    return TemplateResponse(request, 'people_list.html', {'users': User.objects.all()})
    
