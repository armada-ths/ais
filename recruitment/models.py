from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
from django.contrib.auth.models import Group, User

# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')


    def __str__(self):
        return '%s: %s' % (self.fair.name, self.name)


class RecruitableRole(models.Model):
    role = models.OneToOneField(Group, limit_choices_to={'is_role': True})
    recruitment_period = models.ForeignKey(RecruitmentPeriod)

    def __str__(self):
        return '%s' % (self.role)

class RoleApplication(models.Model):
    recruitableRole = models.ForeignKey(RecruitableRole)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s: %s' % (self.user, self.recruitableRole.role)