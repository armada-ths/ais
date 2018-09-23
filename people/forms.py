from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Profile

class ProfileForm(ModelForm):
	def is_valid(self):
		valid = super(ProfileForm, self).is_valid()
		
		if not valid: return valid
		
		dietary_restrictions = self.cleaned_data.get('dietary_restrictions')
		no_dietary_restrictions = self.cleaned_data.get('no_dietary_restrictions')
		
		if len(dietary_restrictions) == 0 and not no_dietary_restrictions:
			self.add_error('no_dietary_restrictions', 'If you have no dietary restrictions, tick this box to confirm.')
			valid = False
		
		elif len(dietary_restrictions) != 0 and no_dietary_restrictions:
			self.add_error('no_dietary_restrictions', 'If you have dietary restrictions, you cannot tick this box.')
			valid = False
			
		return valid
	
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = {"user", "picture", "token"}

		widgets = {
			'registration_year': forms.Select(choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)]),
			'birth_date': forms.DateInput(),
			'planned_graduation': forms.Select(choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 10)]),
			'dietary_restrictions': forms.CheckboxSelectMultiple()
		}
		
		labels= {
			'birth_date': 'Birth date (format: 2016-12-24)',
			'picture_original': 'Picture of you',
		}
