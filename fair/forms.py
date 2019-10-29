from django import forms

from .models import FairDay, LunchTicket, Fair, LunchTicketTime


class LunchTicketForm(forms.ModelForm):
	currentFair = Fair.objects.filter(current=True).first()
	day = forms.ModelChoiceField(queryset = FairDay.objects.filter(fair = currentFair), required = True)
	allDays = []
	for fairDay in FairDay.objects.filter(fair = currentFair):
		allDays.append(fairDay)
	time = forms.ModelChoiceField(queryset = LunchTicketTime.objects.filter(day__in = allDays), required = False)
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

		if user is None and email_address is None:
			self.add_error('email_address', 'You must specify an e-mail if you don\'t specify a user.')
			valid = False

		if time is not None and time.day != day:
			self.add_error('time', 'The time needs to be on the same day as the ticket.')
			valid = False

		return valid

	class Meta:
		model = LunchTicket
		fields = ['used', 'company', 'user', 'email_address', 'comment', 'day', 'time', 'dietary_restrictions', 'other_dietary_restrictions']

		labels = {
			'used': 'The ticket has been used'
		}

		widgets = {
			'dietary_restrictions': forms.CheckboxSelectMultiple(),
			'other_dietary_restrictions' : forms.TextInput(),
		}


class LunchTicketSearchForm(forms.Form):
	include_dietary_restrictions = forms.BooleanField(required = False)

	used_status_choices = [
		('USED', 'Used'),
		('NOT_USED', 'Not used')
	]

	used_statuses = forms.MultipleChoiceField(choices = used_status_choices, widget = forms.CheckboxSelectMultiple(), required = False, label = 'Used?')

	sent_status_choices = [
		('SENT', 'Sent'),
		('NOT_SENT', 'Not sent')
	]

	sent_statuses = forms.MultipleChoiceField(choices = sent_status_choices, widget = forms.CheckboxSelectMultiple(), required = False, label = 'Sent?')

	type_choices = [
		('STUDENT', 'Student'),
		('COMPANY', 'Company')
	]

	types = forms.MultipleChoiceField(choices = type_choices, widget = forms.CheckboxSelectMultiple(), required = False)

	days = forms.ModelMultipleChoiceField(queryset = FairDay.objects.none(), widget = forms.CheckboxSelectMultiple(), label = 'Show only tickets belonging to any of these days', required = False)
