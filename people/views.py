from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
# Create your views here.

def list_people(request):
    if request.user.is_authenticated():
        username = request.user.username
        return TemplateResponse(request, 'people.html', {'users': User.objects.all()})
        #return render(request, 'people.html')
    return render(request, 'login.html')
    
