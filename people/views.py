from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from person.models import Person
# Create your views here.

@login_required(login_url='/login/')
def list_people(request):
    return TemplateResponse(request, 'people_list.html', {'users': User.objects.all()})

@login_required(login_url='/login/')
def view_person(request, pk):
    return TemplateResponse(request, 'view_person.html', {'person': Person.objects.get(id=pk)})
    
