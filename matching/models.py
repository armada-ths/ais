from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.timezone import utc

from enum import Enum, unique


# Matching survey
class Survey(models.Model):
    '''
    relates_to - used to relate the processed survey to the raw survey/the one
    that is used to gather the exhibitor info
    '''
    fair = models.ForeignKey('fair.Fair', default=1)
    name = models.CharField(max_length=256)
    description = models.TextField()

    relates_to = models.ForeignKey('self',null=True, blank=True)

    def __str__(self):
        return "%s at %s"%(self.name, self.fair)

    class Meta:
        ordering = ['name']

CHOICES = (
    (None, '-------'),
    (1, 'Definitely Not'),
    (2, 'Probably Not'),
    (3, 'Maybe'),
    (4, 'Probably'),
    (5,'Definitely')
)

class Question(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    INT = 'integer'
    BOOL = 'boolean'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (SELECT, 'select'),
        (INT, 'integer'),
        (BOOL, 'boolean'),
    )
    name = models.CharField(max_length=64, blank=True, null=True)
    text = models.TextField()
    help_text = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=256, choices=QUESTION_TYPES, blank=True, null=True)
    survey = models.ManyToManyField(Survey)

    def get_choices(self):
        return CHOICES

    def __str__(self):
        return '%s'%self.name
    #class Meta:
    #    ordering = ['name']

class Response(models.Model):
    exhibitor = models.ForeignKey('exhibitors.Exhibitor', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, blank=True, null=True)

    def __str__(self):
        return '%s'%self.exhibitor

class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

class TextAns(Answer):
    ans = models.CharField(null=True, blank=True, max_length=4096)
    #def __str__(self):
    #    return '%s: %s'%(self.question, self.ans)

class ChoiceAns(Answer):
    ans = models.IntegerField(choices=CHOICES, null=True, blank=True)

class IntegerAns(Answer):
    ans = models.IntegerField(null=True, blank=True)

class BooleanAns(Answer):
    ans = models.NullBooleanField(choices=((True,'yes'), (False,'no')), null=True, blank=True)

###########################################################
#   These following questions will contain output processed
#   by the matching algorithm.
#   The answers below are the ones from
#   the app/web, connected to a student_profile.
@unique
class StudentQuestionType(Enum):
    SLIDER = 'slider'
    GRADING = 'grading'

    def is_type(string):
        values = { item.value for item in StudentQuestionType }
        return (string in values)

    def get_choices():
        return [ (question_type.value, question_type.value) for question_type in StudentQuestionType ]


class StudentQuestionBase(models.Model):
    '''
    A base model for all types of student questions.

    ATTENTION! Trying to create an object of this model directly will raise an exception, as it's not intended to be used this way, create an object of one of the children instead!

    This model holds all common information for all types of questions, such as the question string.
    This is to hold all questions in one database, so that we can do more complicated things like rating, ordering or other.

    Additionally child models can be accessed though this one, by calling StudentQuestionBase.childmodelname (note the small case),
    but it might raise a DoesNotExist exception. To avoid this we have a question_type, which should correspond to one of QuestionTypes.
    To see an example please refer to matching/tests.py StudentQuestionTestCase.test_models().

    This database isn't be abstract, as it would make querying and other related code more complicated.
    However, it would be more efficient that way as we wouldn't have a single huge table for all questions with additional tables for extra fields for each question type.

    The student question should be related to a company question via a foregin key, for now it is optional.

    Necessary fields:
        question (string)       - the question
        question_type (string)  - special field that should always correspond to the type of the related questiontype (a child of this model), and as such should not be written to directly
        survey (m2m)            - many-2-many field to Surveys, that use this question

    Optional fields:
        company_question (fk) - foreign key to a company question
    '''

    question = models.CharField(max_length=256)
    question_type = models.CharField(max_length=64, choices=StudentQuestionType.get_choices())
    survey = models.ManyToManyField(Survey, blank=True)
    company_question = models.ForeignKey(Question, blank=True, null=True)
    class Meta:
        default_permissions = ()
        verbose_name = 'question'

    def save(self, *args, **kwargs):
        if StudentQuestionType.is_type(self.question_type):
            return super(StudentQuestionBase, self).save(*args, **kwargs)
        else:
            raise Exception('Trying to save a model <' + str(self) + '> of illegal type \'' + str(self.question_type) + '\'!')
    def __str__(self):
        return 'Question: %s    Type: %s'%(self.question, self.question_type)


class StudentQuestionSlider(StudentQuestionBase):
    '''
    A numerical question answered with a slider.

    Is a child of StudentQuestionBase, which means its fields (question or question_type for example) are also accesable from this model.

    Necessary fields:
        min_value (float)   - the minimal value (left) for the slider
        max_value (float)   - the maximal value (right) for the slider
        units (string)      - the units (plural for now) of the measured entity
    Optional fields:
        logarithmic (bool)  - should the scale be logarithmic (defaults to False)
    '''
    min_value = models.FloatField()
    max_value = models.FloatField()
    units = models.CharField(max_length=64, blank=True, null=True)
    logarithmic = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        verbose_name = 'question slider'
        verbose_name_plural = 'questions slider'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type', None): kwargs.pop('question_type')
        self.question_type = StudentQuestionType.SLIDER.value
        return super(StudentQuestionSlider, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = StudentQuestionType.SLIDER.value
        return super(StudentQuestionSlider, self).save(*args, **kwargs)


class StudentQuestionGrading(StudentQuestionBase):
    '''
    A integer question answered by grading choices (-grading_size/2 to grading_size/2)

    Is a child of StudentQuestionBase, which means its fields (question or question_type for example) are also accesable from this model.

    Necessary field(s):
        grading_size (int) - number of grading choices

    '''
    grading_size = models.IntegerField(default=5)

    class Meta:
        default_permissions = ()
        verbose_name = 'question grading'
        verbose_name_plural = 'questions grading'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type',None): kwargs.pop('question_type')
        self.question_type = StudentQuestionType.GRADING.value
        return super(StudentQuestionGrading, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = StudentQuestionType.GRADING.value
        return super(StudentQuestionGrading, self).save(*args, **kwargs)


class WorkFieldArea(models.Model):
    '''
    Work field main areas. These are manually inputed into the db as a type
    of verification step. To each WorkFieldArea a set of WorkField objects are related

    Necessary field(s):
        work_area (unique string) - work field area name

    Note: work_area is set as unique
    '''
    work_area = models.TextField(unique=True)
    class Meta:
        default_permissions = ()
        verbose_name = 'work field area'
    def __str__(self):
        return '%s'%self.work_area


class WorkField(models.Model):
    '''
    Work fields that are auto created by the matching algorithm. These are
    manually associated via a foregin key to WorkFieldArea as a way of manual
    verification

    Necessary field(s):
        work_field (unique string)  - the work field name

    Optional field(s):
        work_area (fk)              - the work area does not necessary be spec to be in db, (but wont be used in the matching if not)

    Note: the work_field is set as unique and instead the field can be connected
          to multiple surveys if necessary.
    '''
    work_field  = models.TextField(unique=True)
    work_area   = models.ForeignKey(WorkFieldArea, blank=True, null=True)
    survey      = models.ManyToManyField(Survey)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return '%s in %s'%(self.work_field, self.work_area.work_area)


class SwedenRegion(models.Model):
    '''
    Predefined regions in the app. Is used to connect companies cities to student answers in the app.
    region_id is an id that is used to send objects from the app.
    '''
    name = models.TextField()
    region_id = models.IntegerField(unique=True, null=True  )
    survey = models.ManyToManyField(Survey)


    def __str__(self):
        return '%s: %s' %(self.region_id, self.name)


class SwedenCity(models.Model):
    '''
    Used to connect cities to a region in Sweden. Contains preprocessed data.
    '''
    city = models.TextField(unique=True)
    exhibitor = models.ManyToManyField('exhibitors.Exhibitor')
    region = models.ManyToManyField(SwedenRegion)

    class Meta:
            verbose_name = 'sweden city'
            verbose_name_plural = 'sweden cities'

    def __str__(self):
        return self.city


class Continent(models.Model):
    '''
    Connects a exhibitor to a Continent.
    All continents should be connected to at least one exhibitor when used.
    continent_id is an id that is used to send objects from the app.
    '''
    name = models.TextField(unique=True)
    continent_id = models.IntegerField(unique=True, null=True)
    survey = models.ManyToManyField(Survey)

    def __str__(self):
        return '%s: %s' %(self.continent_id, self.name)


class Country(models.Model):
    '''
    Connects Country (that exhibitors work in) to continents (where student want to work)
    '''
    name = models.TextField(unique=True)
    exhibitor = models.ManyToManyField('exhibitors.Exhibitor')
    continent = models.ForeignKey(Continent, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return '%s'%self.name


class JobType(models.Model):
    '''
    All jobtypes connected to an ID.
    LATER:: This should not be used!! Instead jobtypes in exhibitor should be used.
    relates to an exhibitor question for now.
    '''
    job_type = models.TextField()
    job_type_id = models.IntegerField(unique=True)
    exhibitor_question = models.ForeignKey(Question, blank=True, null=True)

    def __str__(self):
        return '%s: %s'%(self.job_type_id, self.job_type)


class StudentAnswerBase(models.Model):
    '''
    Base model for answers to the student questions created by the matching
    algorithm. Contains a timestamp on created/updated that is autosave upon
    save.

    Necessary field(s):
        student (fk)        - foreign key to Student Profile
        survey (m2m)        - related surveys
        created (date-time) - time of creation
        updated (date-time) - time of the last update
    '''
    student = models.ForeignKey('student_profiles.StudentProfile')
    survey = models.ManyToManyField(Survey,blank=True)
    created = models.DateTimeField(editable=False, null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'answer base'
        verbose_name = 'answers base'

    def save(self, *args, **kwargs):
        ''' setting timestamp '''
        if not self.created:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(StudentAnswerBase, self).save(*args, **kwargs)


class StudentAnswerSlider(StudentAnswerBase):
    '''
    A floating point answer model with a foreign key to StudentQuestionSlider

    Parent is StudentAnswerBase

    Necessary field(s):
        question (fk)       - foregin key to StudentQuestionSlider
        answer_min (float)  - the low bound of the range of the answer
        answer_max (float)  - the high bound of the range of the answer
    '''
    question    = models.ForeignKey(StudentQuestionSlider)
    answer_min  = models.FloatField(default=0.0)
    answer_max  = models.FloatField(default=0.0)

    class Meta:
        default_permissions = ()
        verbose_name = 'answer slider'
        verbose_name_plural = 'answers slider'

    def __str__(self):
        return '%.2f to %.2f' % (self.answer_min, self.answer_max)


class StudentAnswerGrading(StudentAnswerBase):
    '''
    A int answer model with a foregin key to StudentAnswerGrading.
    Should be in range: [-grading_size/2 to grading_size/2].

    Is a child of StudentAnswerBase.

    Necessary field(s):
        question (fk)   - foregin key to StudentQuestionGrading
        answer (int)    - answer to question
    '''
    question    = models.ForeignKey(StudentQuestionGrading)
    answer      = models.IntegerField(default=0)

    class Meta:
        default_permissions = ()
        verbose_name = 'answer grading'
        verbose_name_plural = 'answers grading'

    def __str__(self):
        return '%i'%self.answer


class StudentAnswerWorkField(StudentAnswerBase):
    '''
    A boolean answer corresponding to selected WorkField.
    Existance of an instance of this model means that a student selected 'yes' for related WorkField.

    Is a child of StudentAnswerBase.

    Necessary field(s):
        work_field (fk) - a reference to a selected WorkField that a student would prefer to work in.
    '''
    work_field  = models.ForeignKey(WorkField)
    class Meta:
        default_permissions = ()
        verbose_name = 'answer work field'
        verbose_name_plural = 'answers work field'

    def __str__(self):
        return '%s for work field = %s w ans = %s'%(self.student, self.work_field, self.answer)


class StudentAnswerRegion(StudentAnswerBase):
    '''
    A boolean answer corresponding to selected SwedenRegion.
    Existance of an instance of this model means that a student selected 'yes' for related SwedenRegion.

    Is a child of StudentAnswerBase.

    Necessary field(s):
        region (fk) - a reference to a selected SwedenRegion the student would prefer to work in.
    '''
    region = models.ForeignKey(SwedenRegion)

    class Meta:
            verbose_name = 'answer region'
            verbose_name_plural = 'answers region'

    def __str__(self):
        return '%s chose %s' %(self.student, self.region)


class StudentAnswerContinent(StudentAnswerBase):
    '''
    A boolean answer corresponding to selected Continent.
    Existance of an instance of this model means that a student selected 'yes' for related Continent.

    Is a child of StudentAnswerBase.

    Necessary field(s):
        continent (fk)  - a reference to a selected Continent the student would prefer to work in.
    '''
    continent = models.ForeignKey(Continent)

    class Meta:
            verbose_name = 'answer continent'
            verbose_name_plural = 'answers continent'

    def __str__(self):
        return '%s chose %s' %(self.student, self.continent)


class StudentAnswerJobType(StudentAnswerBase):
    '''
    A boolean answer corresponding to selected JobType.
    Existance of an instance of this model means that a student selected 'yes' for related JobType.

    Is a child of StudentAnswerBase.

    Necessary field(s):
        job_type (fk)   - a reference to a selected JobType the student would prefer to get.
    '''
    job_type = models.ForeignKey(JobType, null=True)

    class Meta:
        verbose_name = 'answer job type'
        verbose_name_plural = 'answers job type'

    def __str__(self):
        return '%s chose %s' %(self.student, self.job_type)
