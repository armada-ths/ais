from __future__ import unicode_literals

import datetime
import os.path
from django.utils import timezone
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User, Group
from fair.models import Fair
from companies.models import Company
from people.models import Programme
from forms.models import *

class Role(models.Model):
    name = models.CharField(max_length=100)
    parent_role = models.ForeignKey('Role', null=True, blank=True)
    description = models.TextField(default="", blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.group:
            self.group = Group.objects.get_or_create(name=self.name)[0]
        super(Role, self).save(*args, **kwargs)

    def add_user_to_groups(self, user):
        role = self
        while role != None:
            print(role)
            role.group.user_set.add(user)
            role = role.parent_role
            if role == self:
                break

    class Meta:
        ordering = ['name']
        permissions = (
            ('administer_roles', 'Administer roles'),
        )


    def has_parent(self, other):
        role = self.parent_role
        while role != None:
            if role == other:
                return True
            role = role.parent_role
            if role == self:
                return False
        return False


    def __str__(self):
        return self.name

    def users(self):
        return [application.user for application in RecruitmentApplication.objects.filter(delegated_role=self, status='accepted')]


# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interview_end_date = models.DateTimeField()
    fair = models.ForeignKey(Fair)
    interview_questions = models.ForeignKey(ExtraField, blank=True, null=True)
    application_questions = models.ForeignKey(ExtraField, blank=True, null=True, related_name='application_questions')
    eligible_roles = models.IntegerField(default=3)
    recruitable_roles = models.ManyToManyField(Role)

    class Meta:
        permissions = (
            ('administer_recruitment', 'Administer recruitment'),
        )

    def is_past(self):
        return self.end_date < timezone.now()

    def is_future(self):
        return self.start_date > timezone.now()

    def save(self, *args, **kwargs):
        if not self.interview_questions:
            self.interview_questions = ExtraField.objects.create()
        if not self.application_questions:
            self.application_questions = ExtraField.objects.create()
        super(RecruitmentPeriod, self).save(*args, **kwargs)

    def interviewers(self):
        return [application.user for application in RecruitmentApplication.objects.filter(status='accepted', recruitment_period__fair=self.fair, recruitment_period__start_date__lte=self.start_date).prefetch_related('user').order_by('user__first_name', 'user__last_name')]

    def state_choices(self):
        return [('new', 'New'), ('interview_delegated', 'Delegated'),
         ('interview_planned', 'Planned'), ('interview_done', 'Done'),
         ('accepted', 'Accepted'), ('rejected', 'Rejected')]

    def __str__(self):
        return '%s: %s' % (self.fair.name, self.name)
        

class RecruitmentApplication(models.Model):
    recruitment_period = models.ForeignKey(RecruitmentPeriod)
    user = models.ForeignKey(User)
    rating = models.IntegerField(null=True, blank=True)
    interviewer = models.ForeignKey(User, null=True, blank=True, related_name='interviewer')
    exhibitor = models.ForeignKey(Company, null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(null=True, blank=True, max_length=100)
    submission_date = models.DateTimeField(default=timezone.now, blank=True)
    recommended_role = models.ForeignKey(Role, null=True, blank=True)
    delegated_role = models.ForeignKey(Role, null=True, blank=True, related_name='delegated_role')
    superior_user = models.ForeignKey(User, null=True, blank=True, related_name='superior_user')

    statuses = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')]

    status = models.CharField(choices=statuses, null=True, blank=True, max_length=20)

    class Meta:
        permissions = (
            ('administer_recruitment_applications', 'Administer recruitment applications'),
            ('view_recruitment_applications', 'View recruitment applications'),
            ('view_recruitment_interviews', 'View recruitment interviews'),

        )

    def state(self):
        if self.status:
            return self.status
        if self.interviewer:
            if self.interview_date:
                if self.interview_date > timezone.now():
                    return 'interview_planned'
                else:
                    return 'interview_done'
            else:
                return 'interview_delegated'
        else:
            return 'new'


    def roles_string(self):
        return ' '.join(['%d %s' % (role.order+1, role.role.name) for role in self.roleapplication_set.order_by('order')])

    def __str__(self):
        return '%s' % (self.user)

class RecruitmentApplicationComment(models.Model):
    comment = models.TextField(null=True, blank=True)
    recruitment_application = models.ForeignKey(RecruitmentApplication)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User)

class RoleApplication(models.Model):
    class Meta:
        ordering = ['order']
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None)
    role = models.ForeignKey(Role)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.role)