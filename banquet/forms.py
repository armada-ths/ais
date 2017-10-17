from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import BanquetteAttendant, BanquetTable

from enum import Enum
import datetime

# MODEL IMPORTS
from fair.models import Fair
from .models import BanquetteAttendant
from exhibitors.models import Exhibitor, CatalogInfo

class BanquetteAttendantForm(ModelForm):
    """
    A form where certain AIS users can edit (or create) a BanquetteAttendant
    except the fair field. The student_ticket field is redunant but could not
    be removed in migrations due to old data being dependant on it
    """
    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users')
        exhibitors = kwargs.pop('exhibitors')
        tables = kwargs.pop('tables')

        super(BanquetteAttendantForm, self).__init__(*args, **kwargs)

        self.fields['user'].choices = [(None,'----')] + [(user.pk, user.email if not user.get_full_name() else user.get_full_name() ) for user in users]
        self.fields['exhibitor'].choices = [(None,'----')] + [(exhibitor.pk, exhibitor.__str__()) for exhibitor in exhibitors]
        self.fields['table'].choices = [(None,'----')] + [(table.pk, table.__str__()) for table in tables]
        self.fields['wants_vegan_food'].help_text = "This evening, everyone will be served a delicious three-course lacto-ovo vegetarian dinner to go along with THS Armada's sustainability work"
    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair', 'student_ticket')


class ExternalBanquetSignupForm(ModelForm):
    """
    A form where external users (students, people not from KTH) can signup for the Banquet.
    """
    def __init__(self, *args, **kwargs):
        super(ExternalBanquetSignupForm, self).__init__(*args, **kwargs)
        self.fields['wants_vegan_food'].help_text = "This evening, everyone will be served a delicious three-course lacto-ovo vegetarian dinner to go along with THS Armada's sustainability work"

    class Meta:
        model = BanquetteAttendant
        fields = '__all__'
        exclude = ('fair','user', 'email', 'exhibitor', 'table', 'seat_number', 'ignore_from_placement', 'student_ticket', 'ticket', 'confirmed')
