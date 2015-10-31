from django.forms import ModelForm
from locations.models import Location
from django import forms

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name","room","floor","building","address","capacity","description"]