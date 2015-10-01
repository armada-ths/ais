from django.conf import settings
from django.db import models

# TODO fix view
# https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/
# http://pythoncentral.io/how-to-use-python-django-forms/
class Profile(models.Model):
    #defining shirt sizes
    SHIRT_SIZES = (
        ('WXS', 'Woman X-Small'),
        ('WS', 'Woman Small'),
        ('WM', 'Woman Medium'),
        ('WL', 'Woman Large'),
        ('WXL', 'Woman X-Large'),
        ('MXS', 'Man X-Small'),
        ('MS', 'Man Small'),
        ('MM', 'Man Medium'),
        ('ML', 'Man Large'),
        ('MXL', 'Man X-Large'),
    )

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=-1, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES,blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    drivers_license = models.CharField(max_length=10, null=True,blank=True)
    allergy = models.CharField(max_length=30, null=True,blank=True)
    programme = models.CharField(max_length=30, null=True,blank=True)
    registration_year = models.IntegerField(null=True,blank=True)
    planned_graduation = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return '%s' % (self.user.get_full_name())
