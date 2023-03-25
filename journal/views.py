import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from people.models import Profile
from recruitment.models import RecruitmentApplication
from fair.models import Fair
from .forms import TokenForm


def start(request):
    fair = get_object_or_404(Fair, current=True)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)

    form = TokenForm(request.POST or None)

    if request.POST and form.is_valid():
        if form.cleaned_data["action"] == "REMOVE":
            profile.token = None

        elif form.cleaned_data["action"] == "RENEW":
            profile.token = uuid.uuid4()

        profile.save()

    return render(
        request, "journal/start.html", {"fair": fair, "profile": profile, "form": form}
    )


def ics(request, user_pk, token):
    fair = get_object_or_404(Fair, current=True)
    user = get_object_or_404(User, pk=user_pk)
    profile = get_object_or_404(Profile, user=user, token=token)

    return render(
        request,
        "journal/ics.html",
        {
            "fair": fair,
            "interviews": (
                RecruitmentApplication.objects.filter(interviewer=user)
                | RecruitmentApplication.objects.filter(interviewer2=user)
                | RecruitmentApplication.objects.filter(user=user)
            ).all(),
            "profile": profile,
        },
        content_type="text/plain",
    )
