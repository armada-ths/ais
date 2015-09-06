from django.shortcuts import render
from django.http import HttpResponse
from threading import Thread

def index(request):
    #if request.user.is_authenticated():
    #    username = request.user.username
    #    return render(request, 'root.html')
    #return render(request, 'login.html')
    return render(request, 'base.html')
# Create your views here.
