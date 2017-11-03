from django.contrib.auth.models import User
from django.shortcuts import redirect

from .tasks import create_random_user

def test_matching(request, total):
    for i in range(int(total)):
        create_random_user.delay()
    return redirect('/')
