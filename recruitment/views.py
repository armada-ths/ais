from django.shortcuts import render, redirect, get_object_or_404
from .models import RecruitmentPeriod, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, create_project_group, AISPermission, Programme
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from people.models import Profile
from companies.models import Company, CompanyParticipationYear
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.forms import modelform_factory


class RecruitmentPeriodForm(ModelForm):
    class Meta:
        model = RecruitmentPeriod
        fields = '__all__'
        exclude = ('recruitable_roles', 'image', 'interview_questions', 'application_questions')

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_end_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }


def recruitment(request, template_name='recruitment/recruitment.html'):
    return render(request, template_name, {
        'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
        'roles': [{'parent_role': role, 'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for role in Role.objects.filter(parent_role=None)],
    })


def import_members(request):
    if not request.user.is_superuser():
        return HttpResponseForbidden()
    create_project_group()
    return redirect('/recruitment/')


class RecruitmentApplicationSearchForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    submission_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    roles = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

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
        choices=[('', '-------')] + [(i, i) for i in range(2001, timezone.now().year+1)],
        widget = forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    rating = forms.ChoiceField(
        choices=[('', '-------')] + [(i, i) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    state = forms.ChoiceField(
        choices=[('', '-------')] + [('new', 'New'), ('interview_delegated', 'Delegated'), ('interview_planned', 'Planned'), ('interview_done', 'Done'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def applications_matching_search(self, application_list):
        search_form = self
        name = search_form.cleaned_data['name']

        if name:
            application_list = [application for application in application_list if name.lower() in application.user.get_full_name().lower()]

        programme = search_form.cleaned_data['programme']
        if programme:
            application_list = [application for application in application_list if programme == application.user.profile.programme]

        registration_year = search_form.cleaned_data['registration_year']
        if registration_year:
            application_list = [application for application in application_list if int(registration_year) == application.user.profile.registration_year]

        rating = search_form.cleaned_data['rating']
        if rating:
            application_list = [application for application in application_list if int(rating) == application.rating]

        submission_date = search_form.cleaned_data['submission_date']
        if submission_date:
            application_list = [application for application in application_list if submission_date.lower() in date_filter(application.submission_date).lower()]

        roles_string = search_form.cleaned_data['roles']
        if roles_string:
            application_list = [application for application in application_list if roles_string.lower() in application.roles_string().lower()]

        state = search_form.cleaned_data['state']
        if state:
            application_list = [application for application in application_list if state == application.state()]

        return application_list


def recruitment_period(request, pk, template_name='recruitment/recruitment_period.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = [i for i in recruitment_period.recruitmentapplication_set.order_by('-submission_date').all()]

    search_form = RecruitmentApplicationSearchForm(request.GET or None)
    if search_form.is_valid():
        application_list = search_form.applications_matching_search(application_list)

    number_of_applications_per_page = 25
    paginator = Paginator(application_list, number_of_applications_per_page)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        applications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        applications = paginator.page(paginator.num_pages)

    return render(request, template_name, {
        'recruitment_period': recruitment_period,
        'application': recruitment_period.recruitmentapplication_set.filter(user=request.user).first(),
        'interviews': recruitment_period.recruitmentapplication_set.filter(interviewer=request.user).all(),
        'paginator': paginator,
        'applications': applications,
        'now': timezone.now(),
        'search_form': search_form
    })


def roles_new(request, pk=None, template_name='recruitment/roles_form.html'):
    role = Role.objects.filter(pk=pk).first()

    if request.POST and 'administer_roles' in request.user.ais_permissions():
        if not role:
            role = Role()
        role.name = request.POST['name']
        role.description = request.POST['description']
        set_foreign_key_from_request(request, role, 'parent_role', Role)

        for permission in AISPermission.objects.all():
            if permission.codename in request.POST:
                role.permissions.add(permission)
            else:
                role.permissions.remove(permission)

        role.save()

        return redirect('recruitment')


    users = [application.user for application in RecruitmentApplication.objects.filter(delegated_role=role, status='accepted')]

    return render(request, template_name, {
        'role': role,
        'permissions': AISPermission.objects.all(),
        'roles': Role.objects.exclude(pk=role.pk) if role else Role.objects.all(),
        'users': users,
    })


def roles_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if not 'administer_roles' in request.user.ais_permissions():
        return HttpResponseForbidden()
    role.delete()
    return redirect('recruitment')


def recruitment_period_delete(request, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)

    if not 'administer_recruitment' in request.user.ais_permissions():
        return HttpResponseForbidden()
    recruitment_period.delete()
    return redirect('recruitment')


def recruitment_period_edit(request, pk=None, template_name='recruitment/recruitment_period_new.html'):
    if not 'administer_recruitment' in request.user.ais_permissions():
        return HttpResponseForbidden()

    recruitment_period = RecruitmentPeriod.objects.filter(pk=pk).first()
    form = RecruitmentPeriodForm(request.POST or None, instance=recruitment_period)
    roles = []

    for role in Role.objects.all():
        roles.append({'role': role, 'checked': role in recruitment_period.recruitable_roles.all() if recruitment_period else False})

    if form.is_valid():
        recruitment_period = form.save()
        for role in Role.objects.all():
            role_key = 'role_%d' % role.id
            if role_key in request.POST:
                if not role in recruitment_period.recruitable_roles.all():
                    recruitment_period.recruitable_roles.add(role)
            else:
                recruitment_period.recruitable_roles.remove(role)

        recruitment_period.interview_questions.handle_questions_from_request(request, 'interview_questions')
        recruitment_period.application_questions.handle_questions_from_request(request, 'application_questions')
        recruitment_period.save()

        set_image_key_from_request(request, recruitment_period, 'image', 'recruitment')

        return redirect('recruitment_period', pk=recruitment_period.id)
    else:
        print(form.errors)


    return render(request, template_name, {
        'form': form,
        'roles': [{'parent_role': role,
                   'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for
                  role in Role.objects.filter(parent_role=None)],
        'recruitment_period': recruitment_period,
        'interview_questions': [] if not recruitment_period else recruitment_period.interview_questions.customfield_set.all(),
        'application_questions': [] if not recruitment_period else recruitment_period.application_questions.customfield_set.all(),
    })

def recruitment_application_comment_new(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    comment = RecruitmentApplicationComment()
    comment.user = request.user
    comment.recruitment_application = application
    comment.comment = request.POST['comment']
    comment.save()
    return redirect('recruitment_application_interview', application.recruitment_period.pk, application.id)


class ProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['registration_year'].required = True
        self.fields['programme'].required = True
        self.fields['phone_number'].required = True

    class Meta:
        model = Profile
        fields = ('registration_year', 'programme', 'phone_number', 'linkedin_url')

        labels = {
            'linkedin_url': 'Link to your LinkedIn-profile',
        }


        widgets = {
            'registration_year': forms.Select(choices=[('', '--------')]+ [(year, year) for year in range(2000, timezone.now().year+1)], attrs={'required': True}),
            'programme': forms.Select(
                attrs={'required': True}),
            'phone_number': forms.TextInput(attrs={'required': True})
        }




class RoleApplicationForm(forms.Form):

    role1 = forms.ModelChoiceField(label='Role 1', queryset=Role.objects.all(), widget=forms.Select(attrs={'required': True}))
    role2 = forms.ModelChoiceField(label='Role 2', queryset=Role.objects.all(), required=False)
    role3 = forms.ModelChoiceField(label='Role 3', queryset=Role.objects.all(), required=False)


def recruitment_application_new(request, recruitment_period_pk, pk=None, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)

    if not pk:
        recruitment_application = recruitment_period.recruitmentapplication_set.filter(user=request.user).first()

        # If the user already has an application for this period redirect to it
        if recruitment_application:
            return redirect('recruitment_application_new', recruitment_period.pk, recruitment_application.pk)

    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()


    user = recruitment_application.user if recruitment_application else request.user
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        Profile.objects.create(user=user)

    now = timezone.now()

    if recruitment_period.start_date > now:
        return render(request, 'recruitment/recruitment_application_closed.html', {
            'recruitment_period': recruitment_period,
            'message': 'Application has not opened'
        })

    if recruitment_period.end_date < now:
        return render(request, 'recruitment/recruitment_application_closed.html', {
            'recruitment_period': recruitment_period,
            'message': 'Application closed'
        })

    profile_form = ProfileForm(request.POST or None, instance=profile)

    role_form = RoleApplicationForm(request.POST or None)

    for i in range(1, 4):
        key = 'role%d' % i
        role_form.fields[key].queryset = recruitment_period.recruitable_roles
        if recruitment_application:
            role_application = RoleApplication.objects.filter(
                recruitment_application=recruitment_application,
                order=i
            ).first()
            if role_application:
                print('Role', role_application.role, role_application.role.pk)
                role_form.fields[key].initial = role_application.role.pk
                print('initial is', role_form.fields[key].initial)




    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(request, user)
        set_image_key_from_request(request, profile, 'image', 'profile')

        if role_form.is_valid() and profile_form.is_valid():

            if not recruitment_application:
                recruitment_application = RecruitmentApplication()


            recruitment_application.user = user
            recruitment_application.recruitment_period = recruitment_period
            recruitment_application.save()

            recruitment_application.roleapplication_set.all().delete()
            for i in range(1,4):
                key = 'role%d' % i
                role = role_form.cleaned_data[key]
                if role:
                    RoleApplication.objects.create(
                        recruitment_application=recruitment_application,
                        role=role,
                        order=i
                    )


            profile_form.save()
            return redirect('recruitment_period', recruitment_period.pk)

    return render(request, template_name, {
        'application_questions_with_answers': recruitment_period.application_questions.questions_with_answers_for_user(recruitment_application.user if recruitment_application else None),
        'recruitment_period': recruitment_period,
        'roles': recruitment_period.recruitable_roles.all(),
        'profile_form': profile_form,
        'profile': profile,
        'role_form': role_form,
    })


def set_foreign_key_from_request(request, model, model_field, foreign_key_model):
    if model_field in request.POST:
        try:
            foreign_key_id = int(request.POST[model_field])
            role = foreign_key_model.objects.filter(id=foreign_key_id).first()
            setattr(model, model_field, role)
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()

def set_int_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, int(request.POST[model_field]))
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()

def set_string_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, request.POST[model_field])
            model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()

def set_image_key_from_request(request, model, model_field, file_directory):
    image_key = model_field
    if image_key in request.FILES:
        try:
            file = request.FILES[image_key]
            file_extension = file.name.split('.')[-1]
            if file_extension in ['png', 'jpg', 'jpeg']:
                file_path = '%s/%d/image.%s' % (file_directory, model.pk, file_extension)
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                default_storage.save(file_path, ContentFile(file.read()))
                setattr(model, model_field, file_path)
                model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()

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
            'interviewer': forms.Select(choices=[('', '--------')]+ [(year, year) for year in range(2000, timezone.now().year+1)], attrs={'required': True}),
        }

def recruitment_application_interview(request, pk, template_name='recruitment/recruitment_application_interview.html'):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not 'view_recruitment_applications' in request.user.ais_permissions() and application.interviewer != request.user:
        return HttpResponseForbidden()

    interviewers = []
    for period in RecruitmentPeriod.objects.filter(fair=application.recruitment_period.fair):
        if period.start_date <= application.recruitment_period.start_date:
            for period_application in period.recruitmentapplication_set.filter(status='accepted'):
                interviewers.append(period_application.user)
    interviewers.sort(key=lambda x: x.get_full_name())

    exhibitors = [participation.company for participation in
                  CompanyParticipationYear.objects.filter(fair=application.recruitment_period.fair)]


    InterviewPlanningForm = modelform_factory(
        RecruitmentApplication,
        fields=('interviewer', 'interview_date', 'interview_location', 'recommended_role', 'rating') if 'administer_recruitment_applications' in request.user.ais_permissions() else ('interview_date', 'interview_location', 'recommended_role', 'rating'),
        widgets={
            'rating': forms.Select(choices=[(i,i) for i in range(1,6)]),
            'interview_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
    )
    interview_planning_form = InterviewPlanningForm(request.POST or None, instance=application)
    interview_planning_form.fields['recommended_role'].queryset = application.recruitment_period.recruitable_roles
    if 'interviewer' in interview_planning_form.fields:
        interview_planning_form.fields['interviewer'].choices = [('', '---------')]+[(interviewer.pk, interviewer.get_full_name()) for interviewer in interviewers]


    RoleDelegationForm = modelform_factory(
        RecruitmentApplication,
        fields=('delegated_role', 'exhibitor', 'superior_user', 'status'),
    )
    if 'administer_recruitment_applications' in request.user.ais_permissions():
        role_delegation_form = RoleDelegationForm(request.POST or None, instance=application)
        role_delegation_form.fields['delegated_role'].queryset = application.recruitment_period.recruitable_roles
        role_delegation_form.fields['superior_user'].choices = [('', '---------')] + [
                (interviewer.pk, interviewer.get_full_name()) for interviewer in interviewers]
        role_delegation_form.fields['exhibitor'].choices = [('', '---------')] + [
            (exhibitor.pk, exhibitor.name) for exhibitor in exhibitors]
    else:
        role_delegation_form = None

    if request.POST and (application.interviewer == request.user or 'administer_recruitment_applications' in request.user.ais_permissions()):
        application.recruitment_period.interview_questions.handle_answers_from_request(request, application.user)
        if interview_planning_form.is_valid():
            interview_planning_form.save()

            if role_delegation_form:
                if role_delegation_form.is_valid():
                    role_delegation_form.save()
                    return redirect('recruitment_period', pk=application.recruitment_period.pk)
            else:
                return redirect('recruitment_period', pk=application.recruitment_period.pk)


    return render(request, template_name, {
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(application.user),
        'interview_questions_with_answers': application.recruitment_period.interview_questions.questions_with_answers_for_user(application.user),
        'interview_planning_form': interview_planning_form,
        'role_delegation_form': role_delegation_form,
    })


def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not 'administer_recruitment_applications' in request.user.ais_permissions() and recruitment_application.user != request.user:
        return HttpResponseForbidden()
    recruitment_application.delete()
    return redirect('recruitment_period', recruitment_application.recruitment_period.pk)