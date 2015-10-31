from django.db import models
from django.core.urlresolvers import reverse

class Location(models.Model):
    name = models.CharField(max_length=75)
    room = models.CharField(max_length=75)
    floor = models.CharField(max_length=75)
    building = models.CharField(max_length=75)
    address = models.CharField(max_length=75)
    capacity = models.IntegerField(default=1, blank=True, null=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

def get_absolute_url(self):
    return reverse('location.edit', kwargs={'pk': self.pk})