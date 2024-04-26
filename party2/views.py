from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from fair.models import Fair


def party_index(request, year):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk = request.user.pk)

    return render(request, "party/index.html", 
                  {"fair": fair, "user": user, })