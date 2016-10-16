from django.db import models
from datetime import date

class Fair(models.Model):
    name = models.CharField(max_length=100, default="Armada %d"%(date.today().year))
    year = models.IntegerField(default=date.today().year)

    def is_member_of_fair(self, user):
        if user.is_superuser:
            return True
        for recruitment_period in self.recruitmentperiod_set.all():
            if recruitment_period.recruitmentapplication_set.filter(user=user).exists():
                return True
        return False

    def __str__(self):
        return '%s' % self.name
