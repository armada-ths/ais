from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from .models import Survey, Question, Response, Answer, TextAns, ChoiceAns, IntegerAns, BooleanAns

class ResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # pop which survey to pull questions from
        survey = kwargs.pop('survey')
        exhibitor = kwargs.pop('exhibitor')
        questions = kwargs.pop('questions')
        super(ResponseForm, self).__init__(*args, **kwargs)

        self.survey = survey
        self.exhibitor = exhibitor
        self.questions = questions

        #should be moved to a init_question fields foo
        #for q in survey.questions():
        #for i, surv in enumerate(survey):
        for i, q in enumerate(self.questions):
            if q.question_type == Question.TEXT:
                self.fields['question_%d'%q.pk] = forms.CharField(label=q.text)
            elif q.question_type == Question.SELECT:
                self.fields['question_%d'%q.pk] = forms.ChoiceField(label=q.text, choices = q.get_choices())
            elif q.question_type == Question.INT:
                self.fields['question_%d'%q.pk] = forms.IntegerField(label=q.text)
            elif q.question_type == Question.BOOL:
                self.fields['question_%d'%q.pk] = forms.BooleanField(required=False, label=q.text)
        #should init with already answered and saved questions
        #maybe add all as required?
    class Meta:
        model = Response
        fields = '__all__'

    def save(self, commit=True):
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.exhibitor = self.exhibitor
        response.save()

        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith('question_'):
                pass
                # need to save answer object as separate objects for each answer here, do something smart


        return response
