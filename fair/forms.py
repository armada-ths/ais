from django import forms

from .models import FairDay

class LunchTicketSearchForm(forms.Form):
	include_dietary_restrictions = forms.BooleanField(required = False)
	
	status_choices = [
		('USED', 'Used'),
		('NOT_USED', 'Not used')
	]
	
	statuses = forms.MultipleChoiceField(choices = status_choices, widget = forms.CheckboxSelectMultiple(), required = False)
	
	type_choices = [
		('STUDENT', 'Student'),
		('COMPANY', 'Company')
	]
	
	types = forms.MultipleChoiceField(choices = type_choices, widget = forms.CheckboxSelectMultiple(), required = False)
	days = forms.ModelMultipleChoiceField(queryset = FairDay.objects.none(), widget = forms.CheckboxSelectMultiple(), label = 'Show only tickets belonging to any of these days', required = False)
