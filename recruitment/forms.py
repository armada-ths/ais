import re
from django.forms import ModelForm
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.contrib.auth.models import User
import django.forms as forms
from lib.image import UploadToDirUUID

from people.models import Profile
from companies.models import Company
from fair.models import Fair

from .models import RecruitmentPeriod, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, Programme, CustomFieldArgument, CustomFieldAnswer


class RecruitmentPeriodForm(ModelForm):
	class Meta:
		model = RecruitmentPeriod
		fields = '__all__'
		exclude = ['image', 'interview_questions', 'application_questions', 'fair']
		
		widgets = {
			'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
			'end_date': forms.TextInput(attrs={'class': 'datepicker'}),
			'allowed_groups': forms.CheckboxSelectMultiple
		}
		
		labels = {
			'start_date': 'Start date (Format: 2016-12-24 13:37)',
			'end_date': 'End date (Format: 2016-12-24 13:37)'
		}


class CompareForm(forms.Form):
	recruitment_periods = forms.ModelMultipleChoiceField(queryset = RecruitmentPeriod.objects.all(), widget = forms.CheckboxSelectMultiple(), required = True, label = 'Recruitment periods to compare')
	include_late = forms.BooleanField(required = False, label = 'Include late applications, submitted after the end date')


class RecruitmentApplicationSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    submission_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    #roles = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    recommended_role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    priority = forms.ChoiceField(
        choices = [('', 'Any'), (0, 'First'), (1, 'Second'), (2, 'Third')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(), # Necessary?
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    programme = forms.ModelChoiceField(
        queryset=Programme.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    interviewer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    # registration_year = forms.ChoiceField(
    #     choices=[('', '-------')] + [(i, i) for i in range(2001, timezone.now().year + 1)],
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False
    # )

    rating = forms.ChoiceField(
        choices=[('', '-------'), (1, 1), (2, 2), (3, 3), (5, 5)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    state = forms.ChoiceField(

        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def applications_matching_search(self, application_list):
        search_form = self

        name = search_form.cleaned_data['name']
        if name:
            application_list = [application for application in application_list if
                                name.lower() in application.user.get_full_name().lower()]

        programme = search_form.cleaned_data['programme']
        if programme:
            application_list = [application for application in application_list if
                                programme == application.user.profile.programme]

        # registration_year = search_form.cleaned_data['registration_year']
        # if registration_year:
        #     application_list = [application for application in application_list if
        #                         int(registration_year) == application.user.profile.registration_year]

        rating = search_form.cleaned_data['rating']
        if rating:
            application_list = [application for application in application_list if int(rating) == application.rating]

        submission_date = search_form.cleaned_data['submission_date']
        if submission_date:
            application_list = [application for application in application_list if
                                submission_date.lower() in date_filter(
                                    application.submission_date + timezone.timedelta(hours=2), "d M H:i").lower()]

        # roles_string = search_form.cleaned_data['roles']
        # if roles_string:
        #     application_list = [application for application in application_list if
        #                         roles_string.lower() in application.roles_string().lower()]

        interviewer = search_form.cleaned_data['interviewer']
        if interviewer:
            application_list = [application for application in application_list if
                                interviewer == application.interviewer]

        recommended_role = search_form.cleaned_data['recommended_role']
        if recommended_role:
            application_list = [application for application in application_list if
                                recommended_role == application.recommended_role]

        state = search_form.cleaned_data['state']
        if state:
            application_list = [application for application in application_list if state == application.state()]

        # WIP
        # Get role and priority
        priority = (search_form.cleaned_data['priority']) # Django makes this a string even though it's declared an int in the form
        role = search_form.cleaned_data['role']
        # The user has chosen both a role and a priority,
        # filter out the applications where an applicant
        # has chosen exactly that role with that priority.
        if role and priority:
            print((role, priority))
            print([[(roleapp.role, roleapp.order) for roleapp in application.roles] for application in application_list])
            application_list = [application for application in application_list if (role, int(priority)) in [(roleapp.role, roleapp.order) for roleapp in application.roles]]
        # The user has specified a role but not a 
        # priority, filter out the applications
        # that are for that role.
        elif role:
            application_list = [application for application in application_list if role in [roleapp.role for roleapp in application.roles]]
        # The user has chosen a priority but no
        # role... This is probably a rare use case.
        # Filter out applications where any choice
        # with the given priority has been made.
        elif priority:
            application_list = [application for application in application_list if int(priority) in [roleapp.order for roleapp in application.roles]]

        return application_list

class RolesForm(ModelForm):
    class Meta:
        model = Role

        exclude = ('group',)
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(),
        }

def fix_phone_number(n):
	if n is None: return None
	
	n = n.replace(' ', '')
	n = n.replace('-', '')
	
	if n.startswith("00"): n = "+" + n[2:]
	if n.startswith("0"): n = "+46" + n[1:]
	
	return n

class ProfileForm(ModelForm):
	def clean(self):
		super(ProfileForm, self).clean()
		
		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(self.cleaned_data['phone_number'])
		
		return self.cleaned_data
	
	def is_valid(self):
		valid = super(ProfileForm, self).is_valid()
		
		if not valid: return valid
		
		phone_number = self.cleaned_data.get('phone_number')
		
		if phone_number is not None and not re.match(r'\+[0-9]+$', phone_number):
			self.add_error('phone_number', 'Must only contain numbers and a leading plus.')
			valid = False
			
		return valid
	
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		
		self.fields['registration_year'].required = True
		self.fields['programme'].required = True
		self.fields['phone_number'].required = True
		self.fields['picture_original'].required = True
		self.fields['preferred_language'].required = True
	
	class Meta:
		model = Profile
		fields = ['registration_year', 'programme', 'phone_number', 'linkedin_url', 'picture_original', 'preferred_language']
		
		labels = {
			'linkedin_url': 'Link to your LinkedIn profile',
			'picture_original': 'A picture of yourself',
			'preferred_language': 'What language would you prefer to be interviewed in?'
		}
		
		widgets = {
			'registration_year': forms.Select(choices = [('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)], attrs = {'required': True}),
			'programme': forms.Select(attrs={'required': True}),
			'phone_number': forms.TextInput(attrs={'required': True})
		}


class RoleApplicationForm(forms.Form):
    role1 = forms.ModelChoiceField(label='Role 1', queryset=Role.objects.none(), widget=forms.Select(attrs={'required': True}))
    role2 = forms.ModelChoiceField(label='Role 2', queryset=Role.objects.none(), required=False)
    role3 = forms.ModelChoiceField(label='Role 3', queryset=Role.objects.none(), required=False)


class ProfilePictureForm(ModelForm):
    '''
    Simple 1-field form for changing profile picture in interview form
    '''
    class Meta:
        model = Profile
        fields = ('picture_original',)
        labels = {
            'picture_original': 'Profile picture',
        }
