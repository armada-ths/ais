from fair.models import Fair
from banquet.models import BanquetteAttendant
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


fair = Fair.objects.get(current=True)
attendants = BanquetteAttendant.objects.filter(fair=fair)
for attendant in attendants:
    if attendant.user:
        continue
    else:
        if attendant.email:
            try:
                validate_email(attendant.email)
            except ValidationError:
                continue
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
