from django.db import models

class People(models.Model):
    #defining shirt sizes
    SHIRT_SIZES = (
        ('WS', 'Woman Small'),
        ('WM', 'Woman Medium'),
        ('WL', 'Woman Large'),
        ('WXL', 'Woman X-Large'),
        ('MS', 'Man Small'),
        ('MM', 'Man Medium'),
        ('ML', 'Man Large'),
        ('MXL', 'Man X-Large'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    gender = models.CharField(max_length=15)
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)
    phone_number = models.IntegerField()
    drivers_license = models.CharField(max_length=10)
    allergy = models.CharField(max_length=30)
    programme = models.CharField(max_length=30)
    regestration_year = models.IntegerField()
    planned_graduation = models.IntegerField()
