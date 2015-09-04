from django.db import models

class Fair(models.Model):
    name = models.CharField(max_length=100)
