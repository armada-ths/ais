from django.db import models
from datetime import date

class Fair(models.Model):
    name = models.CharField(max_length=100, default="Armada %d"%(date.today().year))
    year = models.IntegerField(default=date.today().year) 
    def __str__(self):
        return '%s'%(self.name)
