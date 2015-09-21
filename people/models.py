from django.conf import settings
from django.db import models

# TODO fix view
# https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/
# http://pythoncentral.io/how-to-use-python-django-forms/
class People(models.Model):
    #defining shirt sizes
    SHIRT_SIZES = (
        ('N', 'None'),
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
        ('U', 'Undefined'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=-1, primary_key=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=1, default='U', choices=GENDERS)
    shirt_size = models.CharField(max_length=3, default='N', choices=SHIRT_SIZES)
    phone_number = models.IntegerField(null=True)
    drivers_license = models.CharField(max_length=10, null=True)
    allergy = models.CharField(max_length=30, null=True)
    programme = models.CharField(max_length=30, null=True)
    registration_year = models.IntegerField(null=True)
    planned_graduation = models.IntegerField(null=True)
    
    def __str__(self):
        return '%s' % (self.user.get_full_name())
