from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, create_project_group
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.core.exceptions import ValidationError
from people.models import Profile

from companies.models import Company, CompanyParticipationYear

import datetime

def user_has_permission(user, needed_permission):
    if user.has_perm(needed_permission):
        return True

    for application in RecruitmentApplication.objects.filter(user=user, status='accepted'):
        if application.recruitment_period.fair.year == datetime.datetime.now().year:
            if application.delegated_role.has_permission(needed_permission):
                return True
    return False

class RecruitmentPeriodForm(ModelForm):
    class Meta:
        model = RecruitmentPeriod
        fields = '__all__'
        exclude = ('recruitable_roles', 'image')

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_questions": forms.HiddenInput(),
            "application_questions": forms.HiddenInput(),
        }


def recruitment(request, template_name='recruitment/recruitment.html'):
    return render(request, template_name, {
        'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
        'roles': [{'parent_role': role, 'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for role in Role.objects.filter(parent_role=None)],
        'can_edit_recruitment_period': user_has_permission(request.user, 'change_recruitmentperiod'),
        'can_edit_roles': user_has_permission(request.user, 'change_group'),
    })


def import_members(request):
    create_project_group()
    return redirect('/recruitment/')


def recruitment_period(request, pk, template_name='recruitment/recruitment_period.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = recruitment_period.recruitmentapplication_set.order_by('user__first_name', 'user__last_name')
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
        'can_edit_recruitment_period': user_has_permission(request.user, 'change_recruitmentperiod'),
        'can_edit_recruitment_application': user_has_permission(request.user, 'change_recruitmentapplication'),
        'application': recruitment_period.recruitmentapplication_set.filter(user=request.user).first(),
        'interviews': recruitment_period.recruitmentapplication_set.filter(interviewer=request.user).all(),
        'paginator': paginator,
        'applications': applications,
        'now': timezone.now()
    })


def roles_new(request, pk=None, template_name='recruitment/roles_form.html'):
    role = Role.objects.filter(pk=pk).first()
    editable = user_has_permission(request.user, 'change_group')

    permissions = [
        {'codename': 'change_recruitmentperiod', 'name': 'Administer recruitment', 'checked': False},
        {'codename': 'change_group', 'name': 'Administer roles', 'checked': False},
        {'codename': 'change_recruitmentapplication', 'name': 'Administer applications', 'checked': False},
    ]

    if role:
        for permission in permissions:
            for role_permission in role.permissions.all():
                if permission['codename'] == role_permission.codename:
                    permission['checked'] = True


    if request.POST and user_has_permission(request.user, 'change_group'):
        if not role:
            role = Role()
        role.name = request.POST['name']
        role.description = request.POST['description']
        if request.POST['parent_role']:
            parent_role_id = int(request.POST['parent_role'])
            role.parent_role = Role.objects.get(pk=parent_role_id)
        role.save()

        for permission in permissions:
            codename = permission['codename']
            permission_object = Permission.objects.get(codename=permission['codename'])
            if codename in request.POST:
                role.permissions.add(permission_object)
                role.save()
            else:
                role.permissions.remove(permission_object)
                role.save()

        return redirect('/recruitment/')


    users = [application.user for application in RecruitmentApplication.objects.filter(delegated_role=role, status='accepted')]

    return render(request, template_name, {
        'role': role,
        'permissions': permissions,
        'roles': Role.objects.exclude(pk=role.pk) if role else Role.objects.all(),
        'users': users,
        'editable': editable
    })



def roles_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if not user_has_permission(request.user, 'change_group'):
        return HttpResponseForbidden()
    role.delete()
    return redirect('/recruitment/')


def recruitment_period_delete(request, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    if not user_has_permission(request.user, 'change_recruitmentperiod'):
        return HttpResponseForbidden()
    recruitment_period.delete()
    return redirect('/recruitment/')


def recruitment_period_edit(request, pk=None, template_name='recruitment/recruitment_period_new.html'):
    if not user_has_permission(request.user, 'change_recruitmentperiod'):
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

        image_key = 'image'
        if image_key in request.FILES:
            file = request.FILES[image_key]
            print(request.FILES[image_key])
            file_path = 'recruitment/%d/image.%s' % (recruitment_period.pk, file.name.split('.')[-1])
            if os._exists(file_path):
                os.remove(file_path)
            default_storage.save(file_path, ContentFile(file.read()))
            recruitment_period.image = file_path
            recruitment_period.save()

        return redirect('/recruitment/%d' % recruitment_period.id)
    else:
        print(form.errors)
        print("Ai'nt no valid form!")


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
    return redirect('/recruitment/%d/application/%d/interview' % (application.recruitment_period.id, application.id))


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('registration_year', 'programme')


@login_required
def recruitment_application_new(request, recruitment_period_pk, pk=None, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)
    now = timezone.now()

    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()


    user = recruitment_application.user if recruitment_application else request.user
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        Profile.objects.create(user=user)
    profile_form = ProfileForm(request.POST or None, instance=profile)

    if profile_form.is_valid():
        profile_form.save()

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




    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(request, request.user)
        if not recruitment_application:
            recruitment_application = RecruitmentApplication()

        recruitment_application.roleapplication_set.all().delete()

        recruitment_application.user = request.user
        recruitment_application.recruitment_period = recruitment_period
        recruitment_application.save()
        for role_number in range(recruitment_period.eligible_roles):
            role_key = 'role_%d' % role_number
            if role_key in request.POST and request.POST[role_key].isdigit():
                role_id = int(request.POST[role_key])
                role_application = RoleApplication()
                role_application.recruitment_application = recruitment_application
                role_application.role = Role.objects.filter(pk=role_id).first()
                role_application.order = role_number
                role_application.save()
        return redirect('/recruitment/%d' % recruitment_period.id)

    chosen_roles = [None for i in range(recruitment_period.eligible_roles)]

    if recruitment_application:
        role_applications = RoleApplication.objects.filter(recruitment_application=recruitment_application).order_by('order')

        for i in range(len(role_applications)):
            chosen_roles[i] = role_applications[i].role

    return render(request, template_name, {
        'application_questions_with_answers': recruitment_period.application_questions.questions_with_answers_for_user(recruitment_application.user if recruitment_application else None),
        'recruitment_period': recruitment_period,
        'chosen_roles': chosen_roles,
        'roles': recruitment_period.recruitable_roles.all(),
        'profile_form': profile_form
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
            print('Role id was not an int')

def set_string_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, request.POST[model_field])
            model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()



def recruitment_application_interview(request, pk, template_name='recruitment/recruitment_application_interview.html'):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not user_has_permission(request.user, 'change_recruitmentapplication') and application.interviewer != request.user:
        return HttpResponseForbidden()

    if request.POST:

        set_foreign_key_from_request(request, application, 'recommended_role', Role)
        set_int_key_from_request(request, application, 'rating')
        set_string_key_from_request(request, application, 'interview_location')
        set_string_key_from_request(request, application, 'interview_date')

        if user_has_permission(request.user, 'change_recruitmentapplication'):
            set_foreign_key_from_request(request, application, 'interviewer', User)
            set_foreign_key_from_request(request, application, 'delegated_role', Role)
            set_foreign_key_from_request(request, application, 'superior_user', User)
            set_foreign_key_from_request(request, application, 'exhibitor', Company)
            set_string_key_from_request(request, application, 'status')


        application.recruitment_period.interview_questions.handle_answers_from_request(request, application.user)
        #application.recruitment_period.application_questions.handle_answers_from_request(request, application.user)

        #application.save()

        #return redirect('/recruitment/%d/application/%d/interview' % (application.recruitment_period.id, application.recruitment_period.id))
    exhibitors = [participation.company for participation in CompanyParticipationYear.objects.filter(fair=application.recruitment_period.fair)]


    class Status:
        def __init__(self, id):
            self.id = id

        def __str__(self):
            return self.id.capitalize() if self.id else 'None'

        def __eq__(self, other):
            return self.id == other.id


    interviewers = []
    for period in RecruitmentPeriod.objects.filter(fair=application.recruitment_period.fair):
        if period.start_date < application.recruitment_period.start_date:
            for period_application in period.recruitmentapplication_set.filter(status='accepted'):
                interviewers.append(period_application.user)

    return render(request, template_name, {
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(application.user),
        'interview_questions_with_answers': application.recruitment_period.interview_questions.questions_with_answers_for_user(application.user),
        'can_edit_recruitment_application': user_has_permission(request.user, 'change_recruitmentapplication'),
        'roles': [role for role in application.recruitment_period.recruitable_roles.all()],
        'users': User.objects.all,
        'ratings': [i for i in range(1,6)],
        'exhibitors': exhibitors,
        'statuses': [Status(status[0]) for status in RecruitmentApplication.statuses],
        'selected_status': Status(application.status),
        'interviewers': interviewers

    })


def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not user_has_permission(request.user, 'change_recruitmentapplication') and recruitment_application.user != request.user:
        return HttpResponseForbidden()
    recruitment_application.delete()
    return redirect('/recruitment/%d' % recruitment_application.recruitment_period.id)