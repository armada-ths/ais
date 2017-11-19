from banquet.models import BanquetteAttendant

for a in BanquetteAttendant.objects.all():
    a.email = a.email.lower()
    a.save()
    try:
        user = a.user
        if user.email == user.username:
            user.username = user.email.lower()
        user.email = user.email.lower()
        user.save()
    except Exception:
        pass
