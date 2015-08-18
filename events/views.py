from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated():
        username = request.user.username
        return render(request, 'events.html')
    return render(request, 'login.html')

# Create your views here.
