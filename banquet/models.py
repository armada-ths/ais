from django.db import models
from django.contrib.auth.models import User
from exhibitors.models import Exhibitor
from fair.models import Fair

class BanquetTable(models.Model):
    fair = models.ForeignKey(Fair, default=1)
    table_name = models.CharField(max_length=60, null=True, blank=True)
    number_of_seats = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["table_name"]

    def __str__(self):
        return '%s' % (self.table_name)

class BanquetTicket(models.Model):
    """
    Banqut ticket. A model to make it possible to administrate ticket types from admin view.
    Not connected to year, because there's no reason to keep ticket types separeted by year.
    """
    name = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return '%s' % (self.name)


class BanquetteAttendant(models.Model):
    fair = models.ForeignKey(Fair, default=1)
    user = models.ForeignKey(User, null=True, blank=True)  # Null for exhibitor representants
    exhibitor = models.ForeignKey(Exhibitor, null=True, blank=True)  # Null for non-exhibitor representants
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    genders = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('not_specify','Prefer not to specify'),
    ]
    gender = models.CharField(choices=genders, max_length=100)
    job_title = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    ticket = models.ForeignKey(BanquetTicket, null=True, blank=True)
    allergies = models.CharField(max_length=1000, blank=True)
    wants_alcohol = models.BooleanField(default=True)
    wants_lactose_free_food = models.BooleanField(default=False)
    wants_gluten_free_food = models.BooleanField(default=False)
    wants_vegan_food = models.BooleanField(default=False)
    table = models.ForeignKey(BanquetTable, null=True, blank=True, on_delete=models.SET_NULL)
    seat_number = models.SmallIntegerField(null=True, blank=True)
    student_ticket = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    ignore_from_placement = models.BooleanField(default=False)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.exhibitor)
