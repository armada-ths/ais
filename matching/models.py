from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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
    ans = models.CharField(null=True, blank=True, max_length=50)
    #def __str__(self):
    #    return '%s: %s'%(self.question, self.ans)

class ChoiceAns(Answer):
    ans = models.IntegerField(choices=CHOICES, null=True, blank=True)

class IntegerAns(Answer):
    ans = models.IntegerField(null=True, blank=True)

class BooleanAns(Answer):
    ans = models.NullBooleanField(choices=((True,'yes'), (False,'no')), null=True, blank=True)
