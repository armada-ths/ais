from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

# Could be two different survey types for students: one short and one long
class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return "%s"%self.name

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None

# should be a category for exhibitors and one for students
class Category(models.Model):
    name = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey)

    def __str__(self):
        return "%s"%self.name

CHOICES = ((1, 'Definitely Not'), (2, 'Probably Not'), (3, 'Maybe'), (4, 'Probably'), (5,'Definitely'))

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
    fair = models.ForeignKey('fair.Fair')
    text = models.TextField()
    category = models.ForeignKey(Category, blank=True, null=True)
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES)
    #SAVE FUNCTION here or in exhibitor?

    def get_choices(self):
        return self.CHOICES

    def __str__(self):
        return '%s'%self.question

class Response(models.Model):
    exhibitor = models.ForeignKey('exhibitors.Exhibitor', on_delete=models.CASCADE)
    question = models.ForeignKey('Question')
    survey = models.ForeignKey(Survey)

    def __str__(self):
        return "response: %s"%self.exhibitor

class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)

class TextAns(Answer):
    answer = models.CharField(null=True, blank=True, max_length=50)
    def __str__(self):
        return '%s: %s'%(self.question, self.answer)

class ChoiceAns(Answer):
    answer = models.IntegerField(choices=CHOICES, null=True, blank=True)
    def __str__(self):
        return '%s: %s'%(self.question, self.answer)

class BooleanAns(Answer):
    answer = models.BooleanField(choices=((True,'yes'),(False,'no')))
    def __str__(self):
        return '%s: %s'%(self.question, self.answer)
