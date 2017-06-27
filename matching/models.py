from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

CHOICES = ((1, 'Definitely Not'), (2, 'Probably Not'), (3, 'Maybe'), (4, 'Probably'), (5,'Definitely'))

class Answer(models.Model):
    question = models.ForeignKey('Question')

class ChoiceAns(Answer):
    answer = models.IntegerField(choices=CHOICES, null=True, blank=True)
    def __unicode__(self):
        return u'%s: %s'%(self.question, self.answer)

class TextAns(Answer):
    answer = models.CharField(null=True, blank=True, max_length=50)
    def __unicode__(self):
        return u'%s: %s'%(self.question, self.answer)

class BooleanAns(Answer):
    answer = models.BooleanField(choices=((True,'yes'),(False,'no')))
    def __unicode__(self):
        return u'%s: %s'%(self.question, self.answer)

class Question(models.Model):
    question = models.CharField(null=True, blank=True, max_length=100)
    ans_type = models.ForeignKey(ContentType,)
    def __unicode__(self):
        return u'%s'%self.question

class ExhibitorQuestions(models.Model):
    company = models.ForeignKey('companies.Company')
