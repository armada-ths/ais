from django.db import models
from datetime import date
from django.contrib.auth.models import User

class party(models.Model):
    namn = models.CharField(
        max_length=100,
        unique=False,null=False, 
        blank=False
        )
    
    year = models.IntegerField(default=date.today().year)

    party_goers = models.ManyToManyField(
        User,
        blank=True,
        help_text="Fun people who likes to party",
    )

    def __str__(self):
        return "%s for year %s" % (self.namn, self.year)
