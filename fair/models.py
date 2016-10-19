from django.db import models
from datetime import date
from lib.image import UploadToDirUUID


class Fair(models.Model):
    name = models.CharField(max_length=100, default="Armada %d"%(date.today().year))
    year = models.IntegerField(default=date.today().year)

    def is_member_of_fair(self, user):
        if user.is_superuser:
            return True
        for recruitment_period in self.recruitmentperiod_set.all():
            if recruitment_period.recruitmentapplication_set.filter(user=user, status='accepted').exists():
                return True
        return False

    def __str__(self):
        return '%s' % self.name


class Partner(models.Model):
    name = models.CharField(max_length=50)
    fair = models.ForeignKey(Fair)
    logo = models.ImageField(
            upload_to=UploadToDirUUID('partners', 'logo')
            )
    url = models.CharField(max_length=300)
    main_partner = models.BooleanField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name
