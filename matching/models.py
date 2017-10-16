from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.timezone import utc

from enum import Enum, unique


# Matching survey
class Survey(models.Model):
    fair = models.ForeignKey('fair.Fair', default=1)
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return "%s"%self.name

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
#   Thes following question will contain output processed
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

    This is to hold all questions in one database, so that we can do more complicated things like rating, ordering or other.
    This model holds all common information for all types of questions, such as the question string.

    Additionally child models can be accessed though this one, by calling StudentQuestionBase.childmodelname (note the small case),
    but it might raise a DoesNotExist exception. To avoid this we have a question_type, which should correspond to one of QuestionTypes.
    To see an example please refer to matching/tests.py StudentQuestionTestCase.test_models().

    This database isn't be abstract, as it will make querying and other related code more complicated.
    However, it would be more efficient that way as we wouldn't have a single huge table for all questions with additional tables for extra fields for each question type.

    Necessary fields:
        question (string) - the question
        question_type (string) - special field that should always correspond to the type of the related questiontype (a child of this model), and as such should not be written to directly
        fair (Fair) - the fair the question was intended for
    '''

    question = models.CharField(max_length=256)
    question_type = models.CharField(max_length=64, choices=StudentQuestionType.get_choices())
    survey = models.ManyToManyField(Survey)

    class Meta:
        default_permissions = ()
        verbose_name = 'question'

    def save(self, *args, **kwargs):
        if StudentQuestionType.is_type(self.question_type):
            return super(StudentQuestionBase, self).save(*args, **kwargs)
        else:
            raise Exception('Trying to save a model <' + str(self) + '> of illegal type \'' + str(self.question_type) + '\'!')
    def __str__(self):
        return '%s of type %s for %s'%(self.question, self.question_type, self.survey)


class StudentQuestionSlider(StudentQuestionBase):
    '''
    A numerical question answered with a slider.

    Is a child of StudentQuestionBase, which means its fields (question or question_type for example) are also accesable from this model.

    Necessary fields:
        min_value (float) - the minimal value (left) for the slider
        max_value (float) - the maximal value (right) for the slider
    Optional fields:
        step (float) - the step of the slider
    '''
    min_value = models.FloatField()
    max_value = models.FloatField()
    step = models.FloatField(blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'slider question'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type', None): kwargs.pop('question_type')
        self.question_type = StudentQuestionType.SLIDER.value
        return super(StudentQuestionSlider, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = StudentQuestionType.SLIDER.value
        if not step:
            self.step = self.max_value - self.min_value
        return super(StudentQuestionSlider, self).save(*args, **kwargs)


class StudentQuestionGrading(StudentQuestionBase):
    '''
    A integer question answered by grading choices (0-grading_size)

    Parent is StudentQuestionBase

    Necessary field(s):
        grading_size (int) - number of grading choices

    '''
    grading_size = models.IntegerField(default=5)

    class Meta:
        default_permissions = ()
        verbose_name = 'grading question'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type',None): kwargs.pop('question_type')
        self.question_type = StudentQuestionType.GRADING.value
        return super(StudentQuestionGrading, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = StudentQuestionType.GRADING.value
        return super(StudentQuestionGrading, self).save(*args, **kwargs)


class StudentAnswerBase(models.Model):
    '''
    Base model for answers to the student questions created by the matching
    algorithm. Contains a timestamp on created/updated that is autosave upon
    save.

    Necessary field(s):
        student (fk)    - foreign key to Student Profile
    '''
    student = models.ForeignKey('student_profiles.StudentProfile')
    created = models.DateTimeField(editable=False, null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'answer_base'

    def save(self, *args, **kwargs):
        ''' setting timestamp '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(StudentAnswerBase, self).save(*args, **kwargs)

class StudentAnswerSlider(StudentAnswerBase):
    '''
    A floating point answer model with a foreign key to StudentQuestionSlider

    Parent is StudentAnswerBase

    Necessary field(s):
        question        - foregin key to StudentQuestionSlider
        answer (float)  - answer to question
    '''
    question    = models.ForeignKey(StudentQuestionSlider)
    answer      = models.FloatField()

    class Meta:
        default_permissions = ()
        verbose_name = 'answer_slider'

class StudentAnswerGrading(StudentAnswerBase):
    '''
    A int answer model with a foregin key to StudentAnswerGrading

    Parent is StudentAnswerBase

    Necessary field(s):
        question        - foregin key to StudentQuestionGrading
        answer (int)    - answer to question
    '''
    question    = models.ForeignKey(StudentQuestionGrading)
    answer      = models.IntegerField()

    class Meta:
        default_permissions = ()
        verbose_name = 'answer_grading'

class WorkFieldArea(models.Model):
    '''
    Work field main areas. These are manually inputed into the db as a type
    of verification step. To each WorkFieldArea a set of WorkField objects are related

    Necessary field(s):
        work_area (text)    - work field area name
    '''
    work_area = models.TextField()
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
        work_field (text)   - the work field name

    Optional field(s):
        work_area (fk)      - the work area does not necessary be spec to be in db
    '''
    work_field  = models.TextField()
    work_area   = models.ForeignKey(WorkFieldArea, blank=True, null=True)
    class Meta:
        default_permissions = ()
        verbose_name = 'work field'

    def __str__(self):
        return '%s in %s'%(self.work_field, self.work_area.work_area)

class StudentAnswerWorkField(StudentAnswerBase):
    '''
    An boolean answer connecting a student_profile to the WorkField model. Is a
    child of StudentAnswerBase.

    Necessary field(s):
        work_field (fk) - foreign key to WorkField
        answer (bool)   - true or false on that work field
    '''
    work_field  = models.ForeignKey(WorkField)
    answer      = models.BooleanField(choices=((True,'yes'), (False,'no')))
    class Meta:
        default_permissions = ()
        verbose_name = 'answer_workfield'

    def __str__(self):
        return '%s for work field = %s w ans = %s'%(self.student, self.work_field, self.answer)
