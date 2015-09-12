from django.forms import ModelForm
from events.models import Event, EventAttendence

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'capacity','description']

class EventAttendenceForm(ModelForm):
    class Meta:
        model = EventAttendence
        fields = ['name', 'mobile']
