from django.db import models

class Fair(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return '%s'%(self.name)
