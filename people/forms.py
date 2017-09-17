from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

        widgets = {
            "registration_year": forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)]),
            "birth_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }
        labels= {
            'birth_date': 'Birth date (format: 2016-12-24)',
            'portrait': 'Picture of you',
        }
