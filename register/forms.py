from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from companies.models import Group, CompanyCustomer

from fair.models import Fair

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "Email"})
        self.fields["password"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "Password", "type" : "password"})

    def clean(self):
        self.cleaned_data["username"] = self.cleaned_data["username"].lower()
        super(LoginForm, self).clean()


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["email"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "Email"})

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
        self.fields["new_password1"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "New Password", "type" : "password"})
        self.fields["new_password2"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "New Password Confirmation", "type" : "password"})

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].label = ""
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
        self.fields["old_password"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "Old Password", "type" : "password"})
        self.fields["new_password1"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "New Password", "type" : "password"})
        self.fields["new_password2"].widget = forms.TextInput(attrs={"class" : "input", "placeholder" : "New Password Confirmation", "type" : "password"})

class RegistrationForm(ModelForm):
	# TODO: this needs to be Fair-specific
	groups = forms.ModelMultipleChoiceField(queryset = Group.objects.filter(allow_registration = True), widget = forms.CheckboxSelectMultiple(), required = False)
	
	class Meta:
		model = CompanyCustomer
		fields = ("groups",)
	
	agreement_accepted = BooleanField(required=True)
	agreement_accepted.label = "I have read the contract and agree to terms*"
	
	gdpr_accepted = BooleanField(required=True)
	gdpr_accepted.label = "I accept that my personal information is treated in accordance with GDPR*"
	
	authorized_accepted = BooleanField(required=True)
	authorized_accepted.label = "I am authorized to register my company for Armada 2018 and sign this contract*"
