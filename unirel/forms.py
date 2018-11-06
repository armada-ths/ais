from django import forms
import re

from .models import Participant


def fix_phone_number(n):
	if n is None: return None
	
	n = n.replace(' ', '')
	n = n.replace('-', '')
	
	if n.startswith("00"): n = "+" + n[2:]
	if n.startswith("0"): n = "+46" + n[1:]
	
	return n


class DietaryRestrictionsTableForm(forms.Form):
	addon_sleep = forms.BooleanField(required = False, label = 'Only those who are sleeping here')
	addon_lunch = forms.BooleanField(required = False, label = 'Only those who are eating lunch here')
	addon_banquet = forms.BooleanField(required = False, label = 'Only those who attend our banquet')


class ParticipantForm(forms.ModelForm):
	def clean(self):
		super(ParticipantForm, self).clean()
		
		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(self.cleaned_data['phone_number'])
		
		return self.cleaned_data
	
	def is_valid(self):
		valid = super(ParticipantForm, self).is_valid()
		
		if not valid: return valid
		
		phone_number = self.cleaned_data.get('phone_number')
		
		if phone_number is not None and not re.match(r'\+[0-9]+$', phone_number):
			self.add_error('phone_number', 'Must only contain numbers and a leading plus.')
			valid = False
			
		return valid
	
	class Meta:
		model = Participant
		fields = ['company', 'name', 'email_address', 'phone_number', 'addon_banquet', 'addon_sleep', 'addon_lunch', 'dietary_restrictions']
		
		widgets = {
			'addon_banquet': forms.CheckboxInput(),
			'addon_sleep': forms.CheckboxInput(),
			'addon_lunch': forms.CheckboxInput(),
			'dietary_restrictions': forms.CheckboxSelectMultiple(),
		}
		
		labels = {
			'addon_banquet': 'I want to attend the University Relations Banquet (included!)',
			'addon_sleep': 'I want THS Armada to arrange a place for me to sleep (included!)',
			'addon_lunch': 'I want to eat lunch on THS Armada\'s restaurant with company representatives (+ SEK 125)'
		}
		
		help_texts = {
			'addon_sleep': 'If you have friends or relatives in Stockholm, you might want to sleep at their place.',
			'addon_lunch': 'If you choose not to eat on our restaurant, you will be served a lighter lunch, which is included.'
		}
