from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
from django.contrib.auth.models import Group, User
import datetime

# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')

    gender = models.IntegerField(choices=((0, 'male'), (1, 'female')), default=0)

    def __str__(self):
        return '%s: %s' % (self.fair.name, self.name)

class RecruitmentApplication(models.Model):
    recruitmentPeriod = models.ForeignKey(RecruitmentPeriod)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=1)
    submissionDate = models.DateField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return '%s' % (self.user)

class RecruitableRole(models.Model):
    role = models.ForeignKey(Group, limit_choices_to={'is_role': True})
    recruitment_period = models.ForeignKey(RecruitmentPeriod)

    def __str__(self):
        return '%s' % (self.role)



class RoleApplication(models.Model):
    recruitmentApplication = models.ForeignKey(RecruitmentApplication, default=None)
    recruitableRole = models.ForeignKey(RecruitableRole)

    def __str__(self):
        return '%s' % (self.recruitableRole.role)


class InterviewQuestion(models.Model):
    TEXT_FIELD = 0
    CHECK_BOX = 1
    TEXT_AREA = 2
    RADIO_BUTTONS = 3
    FILE = 4

    question = models.CharField(max_length=1000)
    recruitmentPeriod = models.ForeignKey(RecruitmentPeriod)
    arguments = models.CharField(max_length=1000, blank=True)
    fieldType = models.IntegerField(choices=((TEXT_FIELD, 'Text field'), (CHECK_BOX, 'Check boxes'), (TEXT_AREA, 'Text area'), (RADIO_BUTTONS, 'Radio buttons'), (FILE, 'File')), default=TEXT_FIELD)


    def arguments_as_list(self):
        return self.arguments.split(',')

    def __str__(self):
        return '%s' % (self.question)

class InterviewQuestionAnswer(models.Model):
    interviewQuestion = models.ForeignKey(InterviewQuestion)
    recruitmentApplication = models.ForeignKey(RecruitmentApplication)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return '%s' % (self.answer)