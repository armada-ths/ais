from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
from django.contrib.auth.models import Group, User
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os.path

def create_group(group_name):
    group = Group()
    group.name = group_name
    group.is_role = True
    group.save()

hosts_string = 'Photographer, Banquet Host, Banquet Host: Entertainment, Event Host, Lounge Host, Service Host, Career Fair Host, Task force and University Relations Host'
hosts = [role.strip() for role in hosts_string.split(',')]

team_leaders_string = 'Developer: Android , Developer: Back End , Developer: Front End , Developer: iOS, Developer: Systems, Film Team Coordinator, Graphic designer, Green Room Creator, Marketing Coordinator, Photo Team Coordinator , Sponsorship Coordinator, Team Leader: Banquet Entertainment, Team Leader: Banquet Logistics, Team Leader: Banquet Interior, Team Leader: Banquet Technology, Team Leader: Career Fair , Team Leader: Events, Team Leader: Logistics Task Force, Team Leader: Lounches, Team Leader: Service, Team Leader: Technical Task Force, Team Leader: University Relations, Team Leader: University Relations Banquet and Web-TV Coordinator'
team_leaders = [role.strip() for role in team_leaders_string.split(',')]

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
            # print(question)
            if question.id not in question_ids:
                question.delete()

        for question_id in question_ids:
            custom_field = CustomField.objects.filter(pk=question_id).first()
            if not custom_field:
                custom_field = CustomField()

            custom_field.extra_field = extra
            custom_field.question = request.POST['%s_%d' % (field_name, question_id)]
            custom_field.field_type = request.POST['%s-type_%d' % (field_name, question_id)]
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
                    custom_field_argument.save()

    def handle_answers_from_request(self, request):
        extra_field = self
        print(request.FILES)
        print("Number of extra fields: %d" % len(extra_field.customfield_set.all()))

        for custom_field in extra_field.customfield_set.all():
            key = '%s' % (custom_field.id,)
            print('looking for key: %s' % key)
            if custom_field.field_type == 'file' or custom_field.field_type == 'image':
                print("looking for %s" % custom_field.field_type)
                if key in request.FILES:
                    file = request.FILES[key]
                    print(request.FILES[key])
                    file_path = 'custom-field/%d_%s.%s' % (request.user.id, key, file.name.split('.')[-1])
                    path = default_storage.save(file_path, ContentFile(file.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                    print(tmp_file)

                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=request.user
                    )
                    answer.answer = file_path
                    answer.save()
            else:
                if key in request.POST:
                    print("FOUND %s - %s" % (key, request.POST[key]))
                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=request.user
                    )
                    answer_string = request.POST[key]
                    print(key + " " + answer_string)

                    if answer_string:
                        answer.answer = answer_string
                        answer.save()

                else:
                    CustomFieldAnswer.objects.filter(
                        custom_field=custom_field,
                        user=request.user
                    ).delete()


# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interview_end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')
    interview_questions = models.ForeignKey(ExtraField, blank=True, null=True)
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
    rating = models.IntegerField(null=True, blank=True)
    interviewer = models.ForeignKey(User, null=True, blank=True, related_name='interviewer')
    interview_date = models.CharField(null=True, blank=True, max_length=100)
    interview_location = models.CharField(null=True, blank=True, max_length=100)
    submission_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    recommended_role = models.ForeignKey(RecruitableRole, null=True, blank=True)
    delegated_role = models.ForeignKey(RecruitableRole, null=True, blank=True, related_name='delegated_role')
    superior_user = models.ForeignKey(User, null=True, blank=True, related_name='superior_user')

    statuses = [
        ('undecided', 'Undecided'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')]

    status = models.CharField(choices=statuses, default='undecided', max_length=20)

    def __str__(self):
        return '%s' % (self.user)

class RoleApplication(models.Model):
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None)
    recruitable_role = models.ForeignKey(RecruitableRole)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.recruitable_role.role)


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