from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from companies.models import Group, Company
from exhibitors.models import Exhibitor

from fair.models import Fair

class CompleteCompanyDetailsForm(ModelForm):
	class Meta:
		model = Company
		fields = ['name', 'identity_number']

	def is_valid(self, company):
		valid = super(CompleteCompanyDetailsForm, self).is_valid()
		
		if not valid:
			return valid
		
		identity_number = self.cleaned_data.get('identity_number')
		
		if identity_number is not None and Company.objects.filter(identity_number = identity_number).exclude(pk = (company.pk if company else None)).exists():
			self.add_error('identity_number', 'The identity number is used by another company.')
			valid = False
			
		return valid

class CompleteExhibitionDetailsForm(ModelForm):
	class Meta:
		model = Exhibitor
		fields = ['electricity_total_power', 'electricity_socket_count', 'electricity_equipment']

class CompleteFinalSubmissionForm(Form):
	authorized = BooleanField(required = True)
	authorized.label = 'I am authorized to register my company for THS Armada 2018 and sign this contract'
	
	contract = BooleanField(required = True)
	contract.label = 'I have read the contract and, on behalf on my company, I agree to the terms'
	
	gdpr = BooleanField(required = True)
	gdpr.label = 'THS Armada would like to process personal data about you and your organization to be able to create the career fair of 2018, in conjunction with complete registration. The data we intend to collect and process is for name, surname, title of your position, phone number and email address. The data will be processed by members in the THS Armada organization and by our external transport partner, Ryska Posten, in purpose to transport your goods. The data will be saved until 2020-08–07 in Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request correction as to what personal data we are processing about you.'

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
	groups = forms.ModelMultipleChoiceField(queryset = Group.objects.filter(allow_registration = True), widget = forms.CheckboxSelectMultiple(), required = False, label = "")
	
	class Meta:
		model = Company
		fields = ("groups",)
	
	agreement_accepted = BooleanField(required = True)
	agreement_accepted.label = "I have read the contract and agree to terms*"
	
	gdpr_accepted = BooleanField(required = True)
	gdpr_accepted.label = "THS Armada would like to process personal data about you and your organization to be able to contact you in conjunction with initial registration, complete registration and send you information regarding the fair of 2018. The data we intend to collect and process is forename, surname, title of your organization, phone number and email adress. You decide for yourself if you want to leave any information to us. The data will only be processed by the project group in Armada, which consists of a total of 18 people, and will be saved until 2020-04-03 in Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request correction as to what personal data we are processing about you.\nI consent for THS Armada to process my personal data in accordance with the above.*"
	
	authorized_accepted = BooleanField(required = True)
	authorized_accepted.label = "I am authorized to register my company for Armada 2018 and sign this contract*"
