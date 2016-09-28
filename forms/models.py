from __future__ import unicode_literals

import datetime
import os.path
from django.utils import timezone
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User, Group

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
        if not request.POST:
            return
        extra = self
        question_ids = []
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
            custom_field.required = '%s-required_%d' % (field_name, question_id) in request.POST
            custom_field.save()

            for argument in custom_field.customfieldargument_set.all():
                if 'argument_%d_%d' % (question_id, argument.id) not in request.POST:
                    argument.delete()

            for key in request.POST:
                argument_key_prefix = 'argument_%d_' % question_id
                key_split = key.split(argument_key_prefix)
                if len(key_split) == 2:
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
            if custom_field.field_type == 'file' or custom_field.field_type == 'image':
                if key in request.FILES:
                    file = request.FILES[key]

                    # Must think about what type of files that can be uploaded - html files lead to security vulnerabilites
                    file_path = 'custom-field/%d_%s.%s' % (user.id, key, file.name.split('.')[-1])
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    path = default_storage.save(file_path, ContentFile(file.read()))
                    os.path.join(settings.MEDIA_ROOT, path)

                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=user
                    )
                    answer.answer = file_path
                    answer.save()
            else:
                if key in request.POST:
                    answer, created = CustomFieldAnswer.objects.get_or_create(
                        custom_field=custom_field,
                        user=user
                    )
                    answer_string = request.POST[key]

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
    question = models.TextField()
    field_type = models.CharField(choices=fields, default='text_field', max_length=20)
    position = models.IntegerField(default=0)
    required = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.question)

    @property
    def form_key(self):
        return 'custom_field_%s' % self.id

class CustomFieldArgument(models.Model):
    value = models.TextField()
    custom_field = models.ForeignKey(CustomField)
    position = models.IntegerField(default=0)

    def user_answer(self, user):
        return CustomFieldAnswer.objects.filter(user=user).first()

    def id_as_string(self):
        return "%s" % self.id

class CustomFieldAnswer(models.Model):
    custom_field = models.ForeignKey(CustomField)
    user = models.ForeignKey(User)
    answer = models.TextField()

    def __str__(self):
        return '%s' % (self.answer)