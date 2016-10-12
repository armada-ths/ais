from django.db import models
from datetime import date
from lib.image import UploadToDirUUID


class Fair(models.Model):
    name = models.CharField(
            max_length=100,
            default="Armada %d" % (date.today().year)
            )
    year = models.IntegerField(default=date.today().year)

    def __str__(self):
        return self.name


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
