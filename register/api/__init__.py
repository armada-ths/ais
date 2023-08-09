from django.contrib.auth.models import User


def get_user(request):
    user = request.user
    if not user.is_authenticated:
        # Todo: This is only for development, remove for prod!!
        user = User.objects.filter(email="dmu0817@3gamma.com").first()
        # return None

    return user
