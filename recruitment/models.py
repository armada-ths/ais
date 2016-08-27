from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from fair.models import Fair
from companies.models import Company
import os.path
from django.utils import timezone

from people.models import Profile, Programme


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
                    file_path = 'custom-field/%d_%s.%s' % (user.id, key, file.name.split('.')[-1])
                    if os._exists(file_path):
                        os.remove(file_path)
                    path = default_storage.save(file_path, ContentFile(file.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

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
    question = models.CharField(max_length=1000)
    field_type = models.CharField(choices=fields, default='text_field', max_length=20)
    position = models.IntegerField(default=0)
    required = models.BooleanField(default=False)

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


class AISPermission(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)

class Role(models.Model):
    name = models.CharField(max_length=100)
    parent_role = models.ForeignKey('Role', null=True, blank=True)
    description = models.CharField(max_length=1000, default="")
    permissions = models.ManyToManyField(AISPermission)

    class Meta:
        ordering = ['name']

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
        if not self.interview_questions:
            self.interview_questions = ExtraField.objects.create()
        if not self.application_questions:
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


    def __str__(self):
        return '%s' % (self.user)

class RecruitmentApplicationComment(models.Model):
    comment = models.CharField(null=True, blank=True, max_length=1000)
    recruitment_application = models.ForeignKey(RecruitmentApplication)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User)

class RoleApplication(models.Model):
    recruitment_application = models.ForeignKey(RecruitmentApplication, default=None)
    role = models.ForeignKey(Role)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.role)


def create_user_and_stuff(username, first_name, last_name, email, role_name, parent_role_name, recruitment_period_name, fair_name):

    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
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
        for line in f:
                if line.strip():
                    values = line.split(',')
                    username = values[0].strip()
                    first_name = values[1].strip()
                    last_name = values[2].strip()
                    email = values[3].strip()
                    role_name = values[4].strip()
                    create_user_and_stuff(username, first_name, last_name, email, role_name, recruitment_period_name, recruitment_period_name + ' ' + str(year), fair_name)


def create_programmes():
    programmes = ["Business IT Engineering (B.Sc)", "Civil Engineering and Urban Management (M.Sc)",
     "Constructional Engineering (B.Sc)", "Design and Product Realisation (M.Sc)",
     "Electrical Engineering (B.Sc, M.Sc)", "Energy & Environment (M.Sc)",
     "Industrial Engineering and Management (M.Sc)", "Information and Communication Technology (B.Sc, M.Sc)",
     "Materials Design and Engineering (M.Sc)", "Media Technology (M.Sc)", "Computer Engineering (B.Sc)",
     "Computer Engineering and Electronics (B.Sc)", "Engineering Physics (M.Sc)", "Mechanical Engineering (B.Sc, M.Sc)",
     "Vehicle Engineering (M.Sc)", "Chemistry and Chemical Engineering (M.Sc)",
     "Computer Science and Engineering (M.Sc)", "Electrical Engineering and Economics (B.Sc)",
     "Engineering and of Education (M.Sc)", "Medical Engineering (M.Sc)", "Microelectronics (M.Sc)",
     "Architecture Programme", "Biotechnology (M.Sc)", "Chemical Engineering (B.Sc)", "Medical Technology (B.Sc)",
     "Property Development & Real Estate (B.Sc)", "Real Estate and Finance (B.Sc)"]

    for programme in programmes:
        if not Programme.objects.filter(name=programme).first():
            Programme.objects.create(name=programme)


import os

def create_armada_year(year):
    directory = os.path.dirname(os.path.abspath(__file__)) + '/Armada' + str(year)
    create_recruitment_period_from_csv(directory+'/pct.csv', 'Project Core Team', year)
    create_recruitment_period_from_csv(directory+'/ept.csv', 'Extended Project Team', year)


def create_armada_hosts():
    hosts_areas = [{"title":"Business relations and events","roles":[{"name":"Event Host","openPositions":12,"description":"THS Armada is more than just a career fair. It also includes events such as the 5 km Armada run, various case solving-challenges and theme lectures. As an Event Host you are a part of the team that makes sure every event is valuable for both students and the participating companies. You prefer to work in a team and you are positive and outgoing. Most of the events will take place before the fair, starting in late October."},{"name":"Lounge Host","openPositions":12,"description":"During the fair, there are two lounges, one in Nymble and one in KTHB available for the exhibitors and all members of the project. As a Lounge Host you are a part of the team that is responsible for the lounge interior and serving of food and beverages. You have a welcoming and service oriented attitude with good social skills. The position involves intensive work during a few days and it is important that you can handle stress and have a positive attitude. There will be early mornings, so it is a plus if you are a morning person."},{"name":"Service Host","openPositions":"12-16","description":"As a Service Host, you are responsible to provide the fair visitors the best service possible. The role includes both work at the information desk, the student lounge and the wardrobes. It’s important that you are service minded, positive and have good communication skills. You prefer to work in a team, are outgoing and have good social skills."},{"name":"Banquet Host","openPositions":8,"altDescription":"THS Banquet and the Club Armada that is taking place after the main dinner seating. The banquet team is responsible for the entire event, including both planning, shaping and running the operative duties before, during and after the banquet at the Ericsson Globe arenas facilities.","description":"Do you want to participate in one of KTH:s biggest event of the year than banquet host is something for you. With over 700 guests and 160 companies THS Armada present the largest university banquet held in Sweden. As a banquet host you will help the banquet team group leaders with the operative management during the banquet evening, this year at Annexet (Globe Arenas). We are therefore searching for an outgoing, driven and communicative person with an interest in events. Managing this kind of big events there are going to pop up unexpected problems so it´s also a plus if you are comfortable in taking own initiatives."},{"name":"Banquet host: Entertainment","openPositions":2,"description":"As a banquet host, where entertainment is the main focus, you will assist the team leader of entertainment. Most important is that the evening schedule is followed and that the entertainment sections are well organized. You will also have direct contact with the banquet compere and possible artists and therefore assist them. During the evening it can be quite stressful so we are searching for an outgoing, structured and communicative person who can handle stressful situations and of course are interested in event and entertainment."}]},{"title":"Logistics and fair","roles":[{"name":"Career Fair Host","openPositions":175,"description":"As a Career Fair Host, you are the exhibiting organisation’s contact person and ultimately the face of THS Armada to them. Before and during the fair you are responsible for the contact with the exhibitor and make sure they get the best service possible. Therefore it is important that you are service-oriented and have a professional attitude. The work of a Career fair host also includes preparing the fair halls in Nymble, KTHB and KTH Entré the weekend before the fair, as well as restore the halls afterwards. You have great social skills and prefer to work in a team."},{"name":"Task Force","openPositions":"10+10","description":"The Task force is the part of THS Armada that work with the logistics and technology before, during and after the fair. The team work together but are divided into two groups with different responsibilities. One part is responsible for the logistics, which includes taking care of the exhibitors goods. The other part is responsible for the technology which among other things includes supplying the exhibitors with electricity. As a part of the Task force you also work to resolve unforeseen problems that arise during the fair. As the role involves a lot of intensive work over a few days it is important that you are positive and want to create a good atmosphere within the team. You have good problem solving skills and are comfortable making your own decisions."},{"name":"University Relations Host","openPositions":"10","description":"Every year, representatives from other universities in Sweden are invited to THS Armada. As a University Relations Host you are a part of the team that welcomes these representatives. The team works together but you are responsible for one university by guiding them through the day and is available for answering any questions they might have. Together with the other host we are also going to held a party for the visiting universities. The work includes preparing and decorating the venue as well as make sure the representatives have the best evening possible. Other desirable qualities is that you prefer to work in a team and have good communication skills as the role includes contact with many different persons."}]},{"title":"Media and Communication","roles":[{"name":"Photographer","openPositions":5,"description":"As a Photographer, you are part of the team that documents everything that happens before and during THS Armada. This includes photographing the different events, the fair and the banquet. In the beginning of October you will also take individual portraits of all the members of the project. As a person you are creative, positive and outgoing. Previous experience of photography and work samples are a plus."},{"name":"Cameraman","openPositions":1,"description":"As the cameraman during the Armada Fair you are responsible for recording the live streamed material used in our Web-TV broadcast. We expect you to be aproblem solver and a team player, but also be able to work independently. Previous experience in video recording is meritorious, especially live-streaming."},{"name":"Audio Technician","openPositions":1,"description":"As the audio technician during the Armada Fair you are responsible for the audio during the live stream recordings. We expect you to have knowledge of audio recording and we want you to be a real team player. It is important that you are an independent worker and a problem solver. Previous experience in audio recording is meritorious."}]}]
    host = Role.objects.filter(name='Host').first()
    if not host:
        host = Role.objects.create(name='Host')
    for area in hosts_areas:
        for role in area['roles']:
            if not Role.objects.filter(name=role['name']).first():
                Role.objects.create(name=role['name'], description=role['description'], parent_role=host)

def create_project_group():
    create_armada_year(2016)
    #create_armada_year(2015)
    create_programmes()
    create_armada_hosts()

    pass



def ais_permissions_for_user(user):
    if user.is_superuser:
        return [permission.codename for permission in AISPermission.objects.all()]
    permissions = []
    for application in RecruitmentApplication.objects.filter(user=user, status='accepted'):
        if application.recruitment_period.fair.year == timezone.now().year:

            # Check all roles and parent roles
            role = application.delegated_role
            while role:
                for permission in role.permissions.all():
                    permissions.append(permission.codename)
                role = role.parent_role
                if role == application.delegated_role:
                    break

    return permissions

User.add_to_class('ais_permissions', ais_permissions_for_user)

