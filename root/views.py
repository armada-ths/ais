from django.shortcuts import render, redirect
from django.http import HttpResponse
from threading import Thread

def index(request):
    if request.user.is_authenticated():
        return redirect('/recruitment')
    return render(request, 'login.html')
# Create your views here.
