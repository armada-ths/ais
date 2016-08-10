from django.shortcuts import render
from django.contrib.auth import login

# Create your views here.
def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']




        print(username)
        print(password)

    return render(request, 'accounts/login.html')