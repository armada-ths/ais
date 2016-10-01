from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from fair.models import Fair

# An 'Event' belongs to a specific 'Fair'
class Event(models.Model):
    # Add event attendence per model
    fair = models.ForeignKey(Fair)
    name = models.CharField(max_length=75)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    capacity = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(blank=True)
    attendence_description = models.TextField(blank=True)
    registration_open = models.DateTimeField()
    registration_last_day = models.DateTimeField()
    registration_last_day_cancel = models.DateTimeField(null=True)
    public_registration = models.BooleanField(default=False)
    allowed_groups = models.ManyToManyField(Group, blank=True)
    

    def __str__(self):
        return '%s'%(self.name)

# An EventQuestion belongs to a specific Event
class EventQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.TextField(blank=False) 
    required = models.BooleanField(default=False)

    def __str__(self):
        return '%s'%(self.question_text)

# An EventAttendence is for a specific User to attend a specific Event
class EventAttendence(models.Model):
    STATUS = (
    ("A","Approved"),
    ("C","Canceled"),
    ("D","Declined"),
    ("S","Submitted"),
    )

    user = models.ForeignKey(User, null=True, default=None, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default="S")

    def __str__(self):
        if self.user != None:
            user = self.user.get_full_name()
        else:
            user = "External user"
        return '%s attending %s'%(user, self.event.name)
    

# An EventAnswer is the answer to a specific EventQuestion for a specific User
class EventAnswer(models.Model):
    question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE)
    attendence = models.ForeignKey(EventAttendence, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)

    def __str__(self):
        return '%s'%(self.question.question_text)

