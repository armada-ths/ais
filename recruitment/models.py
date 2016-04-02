from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
from django.contrib.auth.models import Group

# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')

    def __str__(self):
        return '%s' % (self.name)


class RoleForRecruitmentPeriod(models.Model):
    role = models.ForeignKey(Group)
    recruitment_period = models.ForeignKey(RecruitmentPeriod)

    def __str__(self):
        return '%s' % (self.role)
