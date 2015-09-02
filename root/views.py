from django.shortcuts import render
from django.http import HttpResponse
from lib.banquet_placement import make_placement
from threading import Thread

def index(request):
    if request.user.is_authenticated():
        username = request.user.username
        return render(request, 'root.html')
    t= Thread(target=make_placement)
    t.start()
    return render(request, 'login.html')

# Create your views here.
