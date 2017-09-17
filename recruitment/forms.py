from django.forms import ModelForm
import django.forms as forms

from .models import RecruitmentPeriod, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, \
    create_project_group, Programme, CustomFieldArgument, CustomFieldAnswer
from django.contrib.auth.models import User
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from fair.models import Fair

from django.utils import timezone
from django.template.defaultfilters import date as date_filter



class RecruitmentPeriodForm(ModelForm):
    class Meta:
        model = RecruitmentPeriod
        fields = '__all__'
        exclude = ('recruitable_roles', 'image', 'interview_questions', 'application_questions', 'fair')

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_end_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }
        labels = {
            'start_date': 'Start date (Format: 2016-12-24 13:37)',
            'end_date': 'End date (Format: 2016-12-24 13:37)',
            'interview_end_date': 'Interview end date (Format: 2016-12-24 13:37)',
        }

class RecruitmentApplicationSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    submission_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    roles = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    recommended_role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
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

    registration_year = forms.ChoiceField(
        choices=[('', '-------')] + [(i, i) for i in range(2001, timezone.now().year + 1)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    rating = forms.ChoiceField(
        choices=[('', '-------')] + [(i, i) for i in range(1, 6)],
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

        registration_year = search_form.cleaned_data['registration_year']
        if registration_year:
            application_list = [application for application in application_list if
                                int(registration_year) == application.user.profile.registration_year]

        rating = search_form.cleaned_data['rating']
        if rating:
            application_list = [application for application in application_list if int(rating) == application.rating]

        submission_date = search_form.cleaned_data['submission_date']
        if submission_date:
            application_list = [application for application in application_list if
                                submission_date.lower() in date_filter(
                                    application.submission_date + timezone.timedelta(hours=2), "d M H:i").lower()]

        roles_string = search_form.cleaned_data['roles']
        if roles_string:
            application_list = [application for application in application_list if
                                roles_string.lower() in application.roles_string().lower()]

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

        return application_list

class RolesForm(ModelForm):
    class Meta:
        model = Role

        exclude = ('group',)
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(),
        }

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['registration_year'].required = True
        self.fields['programme'].required = True
        self.fields['phone_number'].required = True

        self.fields['portrait'].label = 'Please upload a picture of yourself'

    class Meta:
        model = Profile
        fields = ('registration_year', 'programme', 'phone_number', 'linkedin_url', 'portrait')

        labels = {
            'linkedin_url': 'Link to your LinkedIn-profile',
        }

        widgets = {
            'registration_year': forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)],
                attrs={'required': True}),
            'programme': forms.Select(
                attrs={'required': True}),
            'phone_number': forms.TextInput(attrs={'required': True})
        }


class RoleApplicationForm(forms.Form):
    role1 = forms.ModelChoiceField(label='Role 1', queryset=Role.objects.all(),
                                   widget=forms.Select(attrs={'required': True}))
    role2 = forms.ModelChoiceField(label='Role 2', queryset=Role.objects.all(), required=False)
    role3 = forms.ModelChoiceField(label='Role 3', queryset=Role.objects.all(), required=False)


## TODO: This is not used, remove it or use it and replace the form that is used in views
class InterviewPlanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InterviewPlanForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RecruitmentApplication
        fields = ('interviewer', 'interview_location', 'interview_date', 'recommended_role', 'rating')

        labels = {
            'linkedin_url': 'Link to your LinkedIn-profile',
        }

        widgets = {
            'interviewer': forms.Select(
                choices=[('', '--------')] + [(year, year) for year in range(2000, timezone.now().year + 1)],
                attrs={'required': True}),
        }


