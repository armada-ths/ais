from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import BanquetteAttendant

from enum import Enum
import datetime

# MODEL IMPORTS
from fair.models import Fair
from .models import BanquetteAttendant
from exhibitors.models import Exhibitor, CatalogInfo

class BanquetteAttendantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users')
        user = kwargs.pop('user')
        self.users_choice = ModelChoiceField(queryset = User.objects.filter(pk__in=users), required=False, initial=user)
        super(BanquetteAttendantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair','users')

class ExternalBanquetSignupForm(ModelForm):
    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair','user', 'exhibitor', 'table_name', 'seat_number', 'ignore_from_placement')
