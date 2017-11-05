from django.forms import ModelForm, formset_factory
from django import forms

from .models import EventAttendence, EventAnswer, Event

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


class EventForm(ModelForm):
    
    class Meta:
        model = Event
        exclude = {'extra_field', 'image', 'fair'}
        widgets = {
            'event_start': forms.DateTimeInput(),
            'event_end': forms.DateTimeInput(),
            'capacity': forms.NumberInput()
        }
        labels = {
            'event_start': 'Event start (format: 2017-12-24 13:37:00)',
            'event_end': 'Event end (format: 2017-12-24 13:37:00)',
            'image_original': 'Event image'
        }
