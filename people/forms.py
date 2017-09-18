from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'picture', 'picture_original',]

        widgets = {
            'registration_year': forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)]),
            'birth_date': forms.DateInput(),
            'planned_graduation': forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 10)]),
            
        }
        labels= {
            'birth_date': 'Birth date (format: 2016-12-24)',
            'portrait': 'Picture of you',
        }
