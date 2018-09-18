from django.forms import ModelForm

from events.models import Event, Team


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'max_capacity', 'allow_join_cr', 'allow_join_s']
