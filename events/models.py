from django.db import models

# Create your models here.

class Event(models.Model):
    name=models.CharField(max_length=75)
    description=models.CharField(max_length=500)
    registration_open_time=models.DateTimeField()
    registration_close_time=models.DateTimeField()
    event_start=models.DateTimeField()
    event_end=models.DateTimeField()
    public_event = models.BooleanField(default=False)
    capacity = models.IntegerField()

class Event_field(models.Model):
    event=models.ForeignKey(Event)
    name=models.CharField(max_length=75)
    data=models.CharField(max_length=200)
    mandatory=models.BooleanField(default=False)
    position_priority=models.IntegerField(default=0)
