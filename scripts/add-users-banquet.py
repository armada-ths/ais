from fair.models import Fair
from banquet.models import BanquetteAttendant
from django.contrib.auth.models import User

attendants = BanquetteAttendant.objects.filter(confirmed=True)
for attendant in attendants:
    if attendant.user:
        continue
    else:
        if attendant.email:
            user = User.objects.filter(email=attendant.email).first()
            if user:
                attendant.user = user
                attendant.save()
            else:
                new_user= User.objects.create_user(username=attendant.email, email=attendant.email, password="Armada17!")
                attendant.user = new_user
                attendant.save()
        else:
            continue
pass
