from django.forms import ModelForm, Textarea
from events.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
