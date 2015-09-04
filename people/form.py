from django import forms
from django.forms import ModelForm
from people.models import People

class PeopleForm(ModelForm):
    class Meta:
        model = People
        fields = fields = '__all__'
