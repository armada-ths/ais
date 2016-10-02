from django.forms import ModelForm, formset_factory
from events.models import EventAttendence, EventAnswer
from django import forms

class AttendenceForm(forms.Form):

    def get_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('question_'):
                yield (self.fields[name].label, self.fields[name].id, value)

    def __init__(self, *args, **kwargs):
        questions_answers = kwargs.pop('questions_answers')
        super(AttendenceForm, self).__init__(*args, **kwargs)
        for i, (question, answer) in enumerate(questions_answers):
            self.fields['question_%s' % i] = forms.CharField(label=question, required=question.required)
            self.fields['question_%s' % i].id = question.id
            self.fields['question_%s' % i].initial = answer.answer if answer else ""
