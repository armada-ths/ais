from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponse("You are logged in as %s, <a href=\"logout\">Logout</a>" % username)
    return render(request, 'login.html')

# Create your views here.
