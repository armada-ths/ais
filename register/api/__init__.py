from django.contrib.auth.models import User
from django.utils import timezone

from fair.models import Fair


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_user(request):
    user = request.user
    if not user.is_authenticated:
        # Todo: remove for prod
        user = User.objects.filter(email="dmu0817@3gamma.com").first()
        # return None

    return user
