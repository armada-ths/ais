from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField
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
    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair',)

class ExternalBanquetSignupForm(ModelForm):
    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair','user', 'exhibitor', 'table_name', 'seat_number', 'ignore_from_placement')
