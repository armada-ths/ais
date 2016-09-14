from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Event(models.Model):
    # Add event attendence per model
    name = models.CharField(max_length=75)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    capacity = models.IntegerField(default=1, blank=True, null=True)
    description = models.TextField(blank=True)
    registration_open = models.DateTimeField()
    registration_last_day = models.DateTimeField()
    registration_last_day_cancel = models.DateTimeField()
    public_registration = models.BooleanField()

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return '%s'%(self.name)

# An event question belongs to a specific event
class EventQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=256)

# An EventAttendence is for a specific User to attend a specific Event
class EventAttendence(models.Model):
    STATUS = (
    ("A","Approved"),
    ("C","Canceled"),
    ("D","Declined"),
    ("S","Submitted"),
    )

    user = models.ForeignKey(User, null=True, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default="S")

    def __unicode__(self):
        return self.name

# An EventAnswer is the answer to a specific EventQuestion for a specific User
class EventAnswer(models.Model):
    question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE)
    attendence = models.ForeignKey(EventAttendence, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)

# Function in model, explore where used and then remove
def get_absolute_url(self):
    return reverse('event_edit', kwargs={'pk': self.pk})

