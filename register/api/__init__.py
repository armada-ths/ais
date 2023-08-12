import os

from django.contrib.auth.models import User
from django.utils import timezone

from fair.models import Fair

is_dev = os.environ["DJANGO_SETTINGS_MODULE"] == "ais.local.settings"


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_user(request):
    user = request.user
    if not user.is_authenticated:
        if is_dev:
            user = User.objects.filter(email="didrik.munther@armada.nu").first()
        else:
            return None

    return user
