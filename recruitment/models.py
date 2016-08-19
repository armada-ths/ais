from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Permission
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from fair.models import Fair
from companies.models import Company
import os.path
from django.utils import timezone

class ExtraField(models.Model):
    def __str__(self):
        return '%d' % (self.id)

    def questions_with_answers_for_user(self, user):
        questions_with_answers = []
        for custom_field in self.customfield_set.all().order_by('position'):
            answer = CustomFieldAnswer.objects.filter(custom_field=custom_field,
                                                      user=user).first()
            questions_with_answers.append((custom_field, answer))
        return questions_with_answers

    def handle_questions_from_request(self, request, field_name):
        extra = self

        question_ids = []
        print("EXTRA_FIELD: " + field_name)
        for key in request.POST:
            question_key_prefix = field_name + '_'
            key_split = key.split(question_key_prefix)
            if len(key_split) == 2:
                question_ids.append(int(key_split[1]))

        for question in extra.customfield_set.all():
            if question.id not in question_ids:
                question.delete()

        for question_id in question_ids:
            custom_field = CustomField.objects.filter(pk=question_id).first()
            if not custom_field:
                custom_field = CustomField()

            custom_field.extra_field = extra
            custom_field.question = request.POST['%s_%d' % (field_name, question_id)]
            custom_field.field_type = request.POST['%s-type_%d' % (field_name, question_id)]
            custom_field.position = int(request.POST['%s-position_%d' % (field_name, question_id)])
            custom_field.save()

            for argument in custom_field.customfieldargument_set.all():
                if 'argument_%d_%d' % (question_id, argument.id) not in request.POST:
                    argument.delete()

            for key in request.POST:
                argument_key_prefix = 'argument_%d_' % question_id
                key_split = key.split(argument_key_prefix)
                if len(key_split) == 2:
                    print(key)
                    print(key_split)
                    argument_id = int(key_split[1])
                    argument_key = 'argument_%d_%d' % (question_id, argument_id)

                    custom_field_argument = CustomFieldArgument.objects.filter(pk=argument_id).first()
                    if not custom_field_argument:
                        custom_field_argument = CustomFieldArgument()

                    custom_field_argument.custom_field = custom_field
                    custom_field_argument.value = request.POST[argument_key]
                    custom_field_argument.position = request.POST['argument_position_%d_%d' % (question_id, argument_id)]
                    custom_field_argument.save()

    def handle_answers_from_request(self, request, user):
        extra_field = self
        for custom_field in extra_field.customfield_set.all():
            key = custom_field.form_key
            print('looking for key: %s' % key)
            if custom_field.field_type == 'file' or custom_field.field_type == 'image':
                print("looking for %s" % custom_field.field_type)
                if key in request.FILES:
                    file = request.FILES[key]
                    print(request.FILES[key])
                    file_path = 'custom-field/%d_%s.%s' % (user.id, key, file.name.split('.')[-1])
                    path = default_storage.save(file_path, ContentFile(file.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                    print(tmp_file)

                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=user
                    )
                    answer.answer = file_path
                    answer.save()
            else:
                if key in request.POST:
                    print("FOUND %s - %s" % (key, request.POST[key]))
                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=user
                    )
                    answer_string = request.POST[key]
                    print(key + " " + answer_string)

                    if answer_string:
                        answer.answer = answer_string
                        answer.save()

                else:
                    CustomFieldAnswer.objects.filter(
                        custom_field=custom_field,
                        user=user
                    ).delete()

class CustomField(models.Model):
    fields = [
        ('text_field', 'Text field'),
        ('check_box', 'Check box'),
        ('text_area', 'Text area'),
        ('radio_buttons', 'Radio buttons'),
        ('select', 'Drop-down list'),
        ('file', 'File'),
        ('image', 'Image')]

    extra_field = models.ForeignKey(ExtraField)
    question = models.CharField(max_length=1000)
    field_type = models.CharField(choices=fields, default='text_field', max_length=20)
    position = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.question)

    @property
    def form_key(self):
        return 'custom_field_%s' % self.id

class CustomFieldArgument(models.Model):
    value = models.CharField(max_length=100)
    custom_field = models.ForeignKey(CustomField)
    position = models.IntegerField(default=0)

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

class Role(models.Model):
    name = models.CharField(max_length=50)
    parent_role = models.ForeignKey('Role', null=True, blank=True)
    description = models.CharField(max_length=300, default="")
    permissions = models.ManyToManyField(Permission)

    def has_permission(self, needed_permission):
        role = self
        while role != None:
            for permission in role.permissions.all():
                if permission.codename == needed_permission:
                    return True

            role = role.parent_role
            if role == self:
                return False
        return False


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
        return '%s' % (self.name)

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

    image = models.CharField(blank=True, null=True, max_length=100)

    def is_past(self):
        return self.end_date < timezone.now()

    def is_future(self):
        return self.start_date > timezone.now()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.interview_questions = ExtraField.objects.create()
            self.application_questions = ExtraField.objects.create()
        super(RecruitmentPeriod, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: %s' % (self.fair.name, self.name)


class RecruitmentApplication(models.Model):
    recruitment_period = models.ForeignKey(RecruitmentPeriod)
    user = models.ForeignKey(User)
    rating = models.IntegerField(null=True, blank=True)
    interviewer = models.ForeignKey(User, null=True, blank=True, related_name='interviewer')
    exhibitor = models.ForeignKey(Company, null=True, blank=True)
    interview_date = models.CharField(null=True, blank=True, max_length=100)
    interview_location = models.CharField(null=True, blank=True, max_length=100)
    submission_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    recommended_role = models.ForeignKey(Role, null=True, blank=True)
    delegated_role = models.ForeignKey(Role, null=True, blank=True, related_name='delegated_role')
    superior_user = models.ForeignKey(User, null=True, blank=True, related_name='superior_user')

    statuses = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')]

    status = models.CharField(choices=statuses, null=True, blank=True, max_length=20)

    def __str__(self):
        return '%s' % (self.user)

class RecruitmentApplicationComment(models.Model):
    comment = models.CharField(null=True, blank=True, max_length=1000)
    recruitment_application = models.ForeignKey(RecruitmentApplication)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    user = models.ForeignKey(User)

class RoleApplication(models.Model):
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None)
    role = models.ForeignKey(Role)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.role)


def create_user_and_stuff(first_name, last_name, email, role_name, parent_role_name, recruitment_period_name, fair_name):
    username = email.split('@')[0]

    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=username,
            is_staff=True,
        )


    fair = Fair.objects.filter(name=fair_name).first()
    if not fair:
        fair = Fair.objects.create(
            year=2016,
            name=fair_name
        )


    parent_role = Role.objects.filter(name=parent_role_name).first()
    if not parent_role and parent_role_name:
        parent_role = Role.objects.create(name=parent_role_name)

    recruitment_period = RecruitmentPeriod.objects.filter(name=recruitment_period_name).first()
    if not recruitment_period:
        recruitment_period = RecruitmentPeriod.objects.create(
            fair=fair,
            name=recruitment_period_name,
            start_date=datetime.datetime(2016, 1, 1),
            end_date=datetime.datetime(2016, 1, 1),
            interview_end_date=datetime.datetime(2016, 1, 1)
        )

    role = Role.objects.filter(name=role_name).first()
    if not role:
        role = Role.objects.create(
            name=role_name,
            parent_role=parent_role,
        )


    recruitable_role = recruitment_period.recruitable_roles.filter(role=role).first()
    if not recruitable_role:
        recruitment_period.recruitable_roles.add(role)

    recruitment_application = RecruitmentApplication.objects.filter(user=user, delegated_role=role)
    if not recruitment_application:
        RecruitmentApplication.objects.create(
            delegated_role=role,
            status='accepted',
            user=user,
            recruitment_period=recruitment_period
        )

def create_recruitment_period_from_csv(file_path, recruitment_period_name, year):
    fair_name = 'Armada ' + str(year)
    with open(file_path, encoding='utf-8') as f:
        first_line = True
        for line in f:
            if not first_line:
                if line.strip():
                    values = line.split(',')
                    full_name = values[0].strip()
                    first_name = full_name.split(' ')[0]
                    last_name = full_name.split(' ')[1]
                    role_name = values[2].strip()
                    email = values[4].strip()
                    create_user_and_stuff(first_name, last_name, email, role_name, recruitment_period_name, recruitment_period_name + ' ' + str(year), fair_name)
            first_line = False


import os

def create_armada_year(year):
    directory = os.path.dirname(os.path.abspath(__file__)) + '/Armada' + str(year)
    create_recruitment_period_from_csv(directory+'/project_group.csv', 'Project Core Team', year)
    create_recruitment_period_from_csv(directory+'/team_leaders.csv', 'Extended Project Team', year)

def create_project_group():
    create_armada_year(2016)
    #create_armada_year(2015)
    pass

