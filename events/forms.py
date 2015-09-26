from django.forms import ModelForm
from events.models import Event, EventAttendence
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name","event_start","event_end","capacity","needs_approval","description","registration_open","registration_last_day","registration_last_day_cancel","roles","make_event_public"]

        widgets = {
        "event_start":forms.TextInput(attrs={'class':'datepicker'}),
        "event_end":forms.TextInput(attrs={'class':'datepicker'}),
        "registration_open":forms.TextInput(attrs={'class':'datepicker'}),
        "registration_last_day":forms.TextInput(attrs={'class':'datepicker'}),
        "registration_last_day_cancel":forms.TextInput(attrs={'class':'datepicker'}),
        }

class EventAttendenceForm(ModelForm):
    class Meta:
        model = EventAttendence
        fields = ["person","status","name","mobile","allergies","attending"]
