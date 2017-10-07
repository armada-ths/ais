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
        exhibitors = kwargs.pop('exhibitors')
        super(BanquetteAttendantForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = [(user.pk, user.get_full_name()) for user in users]
        self.fields['exhibitor'].choices = [(exhibitor.pk, exhibitor.__str__()) for exhibitor in exhibitors]
        self.fields['wants_vegan_food'].help_text = "This evening, everyone will be served a delicious three-course lacto-ovo vegetarian dinner to go along with THS Armada's sustainability work"
    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair', 'student_ticket')


class ExternalBanquetSignupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExternalBanquetSignupForm, self).__init__(*args, **kwargs)
        self.fields['wants_vegan_food'].help_text = "This evening, everyone will be served a delicious three-course lacto-ovo vegetarian dinner to go along with THS Armada's sustainability work"

    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair','user', 'exhibitor', 'table_name', 'seat_number', 'ignore_from_placement', 'student_ticket', 'ticket_type', 'confirmed')
