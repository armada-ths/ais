from django import forms

from .models import FairDay, LunchTicket


class LunchTicketForm(forms.ModelForm):
	def is_valid(self):
		valid = super(LunchTicketForm, self).is_valid()
		
		if not valid: return valid
		
		email_address = self.cleaned_data['email_address']
		company = self.cleaned_data['company']
		user = self.cleaned_data['user']
		day = self.cleaned_data['day']
		time = self.cleaned_data['time']
		
		if company is not None and user is not None:
			self.add_error('company', 'You cannot specify both a company and a user.')
			self.add_error('user', 'You cannot specify both a company and a user.')
			valid = False
		
		if company is None and user is None:
			self.add_error('company', 'You must specify either a company or a user.')
			self.add_error('user', 'You must specify either a company or a user.')
			valid = False
		
		if user is not None and email_address is not None:
			self.add_error('email_address', 'You cannot specify an e-mail address if you specify a user.')
			valid = False
		
		if time is not None and time.day != day:
			self.add_error('time', 'The time needs to be on the same day as the ticket.')
			valid = False
		
		return valid
	
	class Meta:
		model = LunchTicket
		fields = ['used', 'company', 'user', 'email_address', 'comment', 'day', 'time', 'dietary_restrictions']
		
		labels = {
			'used': 'The ticket has been used'
		}
		
		widgets = {
			'day': forms.RadioSelect(),
			'time': forms.RadioSelect(),
			'dietary_restrictions': forms.CheckboxSelectMultiple()
		}


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
