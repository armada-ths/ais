from django.forms import ModelForm, TextInput

from events.models import Event, Team


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = '__all__'
		widgets = {
			'date_start': TextInput(attrs = {'placeholder': '1994-07-12 13:37:00'}),
			'date_end': TextInput(attrs = {'placeholder': '1995-10-10 13:37:00'})
		}


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'max_capacity', 'allow_join_cr', 'allow_join_s']
