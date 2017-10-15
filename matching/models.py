from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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


# These question types are different from matching/models.py as we're interested in more specific options
# More are to follow?
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

    fair = models.ForeignKey('fair.Fair', default=1)

    class Meta:
        default_permissions = ()
        verbose_name = 'question'

    def save(self, *args, **kwargs):
        if StudentQuestionType.is_type(self.question_type):
            return super(StudentQuestionBase, self).save(*args, **kwargs)
        else:
            raise Exception('Trying to save a model <' + str(self) + '> of illegal type \'' + str(self.question_type) + '\'!')


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
    step = models.FloatField(default=1.0, blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'slider question'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type', None): kwargs.pop('question_type')
        self.question_type = StudentQuestionType.SLIDER.value
        return super(StudentQuestionSlider, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = StudentQuestionType.SLIDER.value
        return super(StudentQuestionSlider, self).save(*args, **kwargs)


class StudentQuestionGrading(StudentQuestionBase):
    '''
    Work in progress!

    
    '''

    class Meta:
        default_permissions = ()
        verbose_name = 'grading question'
