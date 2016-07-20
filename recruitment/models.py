from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
from django.contrib.auth.models import Group, User
import datetime


class ExtraField(models.Model):
    def __str__(self):
        return '%d' % (self.id)

    def questions_with_answers_for_user(self, user):
        questions_with_answers = []
        for custom_field in self.customfield_set.all():
            answer = CustomFieldAnswer.objects.filter(custom_field=custom_field,
                                                      user=user).first()
            questions_with_answers.append((custom_field, answer))
        return questions_with_answers

# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')
    extra_field = models.ForeignKey(ExtraField, blank=True, null=True)
    application_questions = models.ForeignKey(ExtraField, blank=True, null=True, related_name='application_questions')
    eligible_roles = models.IntegerField(default=3)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.extra_field = ExtraField.objects.create()
            self.application_questions = ExtraField.objects.create()
        super(RecruitmentPeriod, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: %s' % (self.fair.name, self.name)

class RecruitableRole(models.Model):
    role = models.ForeignKey(Group, limit_choices_to={'is_role': True})
    recruitment_period = models.ForeignKey(RecruitmentPeriod)

    def __str__(self):
        return '%s' % (self.role)


class RecruitmentApplication(models.Model):
    recruitment_period = models.ForeignKey(RecruitmentPeriod)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=1)
    interviewer = models.ForeignKey(User, null=True, blank=True, related_name='interviewer')
    interview_date = models.CharField(null=True, blank=True, max_length=100)
    interview_location = models.CharField(null=True, blank=True, max_length=100)
    submission_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    recommended_role = models.ForeignKey(RecruitableRole, null=True, blank=True)
    delegated_role = models.ForeignKey(RecruitableRole, null=True, blank=True, related_name='delegated_role')
    superior_user = models.ForeignKey(User, null=True, blank=True, related_name='superior_user')

    def __str__(self):
        return '%s' % (self.user)

class RoleApplication(models.Model):
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None)
    recruitable_role = models.ForeignKey(RecruitableRole)

    def __str__(self):
        return '%s' % (self.recruitable_role.role)


class CustomField(models.Model):

    fields = [
        ('text_field', 'Text field'),
        ('check_box', 'Check box'),
        ('text_area', 'Text area'),
        ('radio_buttons', 'Radio buttons'),
        ('file', 'File'),
        ('image', 'Image')]

    extra_field = models.ForeignKey(ExtraField)
    question = models.CharField(max_length=1000)
    field_type = models.CharField(choices=fields, default='text_field', max_length=20)

    def __str__(self):
        return '%s' % (self.question)

class CustomFieldArgument(models.Model):
    value = models.CharField(max_length=100)
    custom_field = models.ForeignKey(CustomField)

    def user_answer(self, user):
        return CustomFieldAnswer.objects.filter(user=user).first()

    def id_as_string(self):
        return "%s" % self.id

class CustomFieldAnswer(models.Model):
    custom_field = models.ForeignKey(CustomField)
    user = models.ForeignKey(User)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return '%s' % (self.answer)