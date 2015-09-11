from django.db import models
from django.core.urlresolvers import reverse

class Event(models.Model):
    name = models.CharField(max_length=75)
    capacity = models.IntegerField(default=1, blank=True, null=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

def get_absolute_url(self):
    return reverse('event_edit', kwargs={'pk': self.pk})

class EventAttendence(models.Model):
    name = models.CharField(max_length=75)
    mobile = models.IntegerField(default=1, blank=True, null=True)

    def __unicode__(self):
        return self.name
