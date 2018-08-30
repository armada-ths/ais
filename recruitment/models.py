from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from fair.models import Fair
from companies.models import Company
import os.path
from django.utils import timezone
from markupfield.fields import MarkupField

from people.models import Programme, Profile

class Location(models.Model):
	name = models.CharField(blank = False, null = False, max_length = 100)
	
	class Meta:
		ordering = ['name']
	
	def __str__(self): return self.name

class Slot(models.Model):
	location = models.ForeignKey(Location, blank = False, null = False, on_delete = models.CASCADE)
	start = models.DateTimeField(blank = False, null = False)
	length = models.PositiveIntegerField(blank = False, null = False, verbose_name = 'Length (minutes)')
	
	class Meta:
		ordering = ['start', 'location']
	
	@property
	def start_iso8601(self): return self.start.isoformat().replace('-', '').replace(':', '').replace('+0000', 'Z')
	
	@property
	def end_iso8601(self): return (self.start + datetime.timedelta(minutes = self.length)).isoformat().replace('-', '').replace(':', '').replace('+0000', 'Z')
	
	def __str__(self):
		nice_start = timezone.localtime(self.start)
		nice_end = timezone.localtime(self.start)
		nice_end += datetime.timedelta(minutes = self.length)
		
		return nice_start.strftime('%Y-%m-%d %H:%M') + ' – ' + nice_end.strftime('%Y-%m-%d %H:%M')

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
                    extension = file.name.split('.')[-1]

                    allowed_extensions = ['pdf', 'png', 'jpg', 'jpeg']
                    if extension in allowed_extensions:
                        file_path = 'custom-field/%d_%s.%s' % (user.id, key, extension)
                        if default_storage.exists(file_path):
                            default_storage.delete(file_path)
                        default_storage.save(file_path, ContentFile(file.read()))

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
                    answer.answer = request.POST[key]
                    answer.save()

                else:
                    CustomFieldAnswer.objects.filter(
                        custom_field=custom_field,
                        user=user
                    ).delete()

class CustomField(models.Model):
    field_types = [
        ('text_field', 'Text field'),
        ('check_box', 'Check box'),
        ('text_area', 'Text area'),
        ('radio_buttons', 'Radio buttons'),
        ('select', 'Drop-down list'),
        ('file', 'File'),
        ('image', 'Image')]

    extra_field = models.ForeignKey(ExtraField, on_delete=models.CASCADE)
    question = MarkupField(markup_type = "markdown")
    field_type = models.CharField(choices=field_types, default='text_field', max_length=20)
    position = models.IntegerField(default=0)
    required = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.question)

    @property
    def form_key(self):
        return 'custom_field_%s' % self.id


class CustomFieldArgument(models.Model):
    value = models.TextField()
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    def user_answer(self, user):
        return CustomFieldAnswer.objects.filter(user=user).first()

    def id_as_string(self):
        return "%s" % self.id

    def __str__(self):
        return '%s - %s' % (self.custom_field, self.value)


class CustomFieldAnswer(models.Model):
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return '%s - %s - %s' % (self.user.get_full_name(), self.custom_field, self.answer)

class RecruitmentPeriod(models.Model):
	name = models.CharField(max_length=30)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	interview_end_date = models.DateTimeField()
	fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
	interview_questions = models.ForeignKey(ExtraField, blank=True, null=True, on_delete=models.CASCADE)
	application_questions = models.ForeignKey(ExtraField, blank=True, null=True, related_name='application_questions', on_delete=models.CASCADE)
	eligible_roles = models.IntegerField(default=3)
	allowed_groups = models.ManyToManyField(Group, blank = True, help_text = 'Only those who are members of at least one of the selected groups can see the applications submitted to this recruitment period.')

	class Meta:
		ordering = ['fair', 'name']
		permissions = (
			('administer_recruitment', 'Administer recruitment'),
		)
	
	@property
	def recruitable_roles(self): return Role.objects.filter(recruitment_period = self)

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
		return str(self.fair.year) + ' – ' + self.name

class Role(models.Model):
	name = models.CharField(max_length = 100)
	parent_role = models.ForeignKey('Role', null=True, blank=True, on_delete=models.CASCADE)
	description = models.TextField(default="", blank=True)
	group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
	organization_group = models.CharField(max_length=100, default='', null=True)
	recruitment_period = models.ForeignKey(RecruitmentPeriod, null = False, blank = False, on_delete = models.CASCADE)
	
	def add_user_to_groups(self, user):
		if self.group is None: return
		
		role = self
		while role != None:
			role.group.user_set.add(user)
			role = role.parent_role
			if role == self:
				break
	
	class Meta:
		ordering = ['recruitment_period', 'organization_group', 'name']
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
		return self.recruitment_period.name + ' – ' + self.name
	
	def users(self):
		return [application.user for application in RecruitmentApplication.objects.filter(delegated_role=self, status='accepted')]

class RecruitmentApplication(models.Model):
	recruitment_period = models.ForeignKey(RecruitmentPeriod, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField(null=True, blank=True)
	interviewer = models.ForeignKey(User, null=True, blank=True, related_name='interviewer', on_delete=models.CASCADE)
	interviewer2 = models.ForeignKey(User, null=True, blank=True, related_name='interviewer2', on_delete=models.CASCADE)
	exhibitor = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
	slot = models.ForeignKey(Slot, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Time and location')
	submission_date = models.DateTimeField(default=timezone.now, blank=True)
	recommended_role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
	delegated_role = models.ForeignKey(Role, null=True, blank=True, related_name='delegated_role', on_delete=models.CASCADE)
	superior_user = models.ForeignKey(User, null=True, blank=True, related_name='superior_user', on_delete=models.CASCADE)
	scorecard = models.CharField(null=True, blank=True, max_length=300)
	drive_document = models.CharField(null=True, blank=True, max_length=300)
	
	@property
	def profile(self): return Profile.objects.filter(user = self.user).first()

	@property
	def roles(self): return self.roleapplication_set.order_by("order")

	statuses = [
		('accepted', 'Accepted'),
		('rejected', 'Rejected'),
		('withdrawn', 'Withdrawn')]

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
			if self.slot:
				if self.slot.start > timezone.now():
					return 'interview_planned'
				else:
					return 'interview_done'
			else:
				return 'interview_delegated'
		else:
			return 'new'


	def roles_string(self):
		return ' '.join(['(%s) %s' % (role.role.organization_group, role.role.name) for role in self.roleapplication_set.order_by('order')])

	def __str__(self):
		return '%s' % (self.user)

class RecruitmentApplicationComment(models.Model):
	comment = models.TextField(null=True, blank=True)
	recruitment_application = models.ForeignKey(RecruitmentApplication, on_delete=models.CASCADE)
	created_date = models.DateTimeField(default=timezone.now, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class RoleApplication(models.Model):
    class Meta:
        ordering = ['order']
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.role)
