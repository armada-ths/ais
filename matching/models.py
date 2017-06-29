from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

# Matching survey
class Survey(models.Model):
    fair = models.ForeignKey('fair.Fair', default=1)
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __unicode__(self):
        return "%s"%self.name

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None

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
    text = models.TextField()
    survey = models.ForeignKey(Survey, blank=True, null=True)
    question_type = models.CharField(max_length=256, choices=QUESTION_TYPES)

    def __unicode__(self):
        return '%s'%self.text

CHOICES = (
    (1, 'Definitely Not'),
    (2, 'Probably Not'),
    (3, 'Maybe'),
    (4, 'Probably'),
    (5,'Definitely')
)

class Response(models.Model):
    exhibitor = models.ForeignKey('exhibitors.Exhibitor', on_delete=models.CASCADE)
    question = models.ForeignKey(Question)
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return '%s'%self.exhibitor

class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)

class TextAns(Answer):
    ans = models.CharField(null=True, blank=True, max_length=50)

class ChoiceAns(Answer):
    ans = models.IntegerField(choices=CHOICES, null=True, blank=True)

class IntegerAns(Answer):
    ans = models.IntegerField(null=True, blank=True)
    #def __unicode__(self):
    #    return '%s: %s'%(self.question, self.ans)

class BooleanAns(Answer):
    ans = models.BooleanField(choices=((True,'yes'),(False,'no')))
