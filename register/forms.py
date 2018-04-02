from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from fair.models import Fair
from orders.models import Product, Order, ProductType
from matching.models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns
from sales.models import Sale
from exhibitors.models import Exhibitor, CatalogInfo
from companies.models import Company, Contact

from enum import Enum
import datetime

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['password'].label = ""
        self.fields['username'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Email'})
        self.fields['password'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Password', 'type' : 'password'})

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        super(LoginForm, self).clean()


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Email'})

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].label = ""
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password', 'type' : 'password'})
        self.fields['new_password2'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password Confirmation', 'type' : 'password'})

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = ""
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].label = ""
        self.fields['old_password'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Old Password', 'type' : 'password'})
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password', 'type' : 'password'})
        self.fields['new_password2'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password Confirmation', 'type' : 'password'})



class RegistrationForm(Form):
    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the binding contract and agree to terms, and I am also authorized to register my organization for THS Armada 2018 and sign this contract.*";
    gdpr_accepted = BooleanField(required=True)
    gdpr_accepted.label = "THS Armada would like to process personal data about you and your organization to be able to contact you in conjunction with initial registration, complete registration and send you information regarding the fair of 2018. The data we intend to collect and process is forename, surname, title of your organization, phone number and email adress. You decide for yourself if you want to leave any information to us. The data will only be processed by the project group in Armada, which consists of a total of 18 people, and will be saved until 2020-04-03 in Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request correction as to what personal data we are processing about you.\nI consent for THS Armada to process my personal data in accordance with the above.*";


class InterestForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('diversity_room','green_room', 'events' )
        labels = {
            "diversity_room": _("Interested in diversity room"),
            "green_room": _("Interested in green room"),
            "events": _("Interested in having events")
        }
        #help_texts = {
        #    "diversity_room": _("Tick this if you are interested in our diversity room concept"),
        #}

