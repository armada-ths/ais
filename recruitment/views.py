from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, RolePermission, create_project_group
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

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

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "interview_questions": forms.HiddenInput(),
            "application_questions": forms.HiddenInput(),
        }


def recruitment(request, template_name='recruitment/recruitment.html'):
    create_project_group()
    return render(request, template_name, {
        'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
        #'roles': Role.objects.all(),
        'roles': [{'parent_role': role, 'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for role in Role.objects.filter(parent_role=None)],
        'can_edit_recruitment_period': user_has_permission(request.user, 'change_recruitmentperiod'),
        'can_edit_roles': user_has_permission(request.user, 'change_group'),
    })


def recruitment_period(request, pk, template_name='recruitment/recruitment_period.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)

    return render(request, template_name, {
        'recruitment_period': recruitment_period,
        'can_edit_recruitment_period': user_has_permission(request.user, 'change_recruitmentperiod'),
        'can_edit_recruitment_application': user_has_permission(request.user, 'change_recruitmentapplication'),
        'application': recruitment_period.recruitmentapplication_set.filter(user=request.user).first(),
        'interviews': recruitment_period.recruitmentapplication_set.filter(interviewer=request.user).all()
    })


def roles_new(request, pk=None, template_name='recruitment/roles_form.html'):
    if not user_has_permission(request.user, 'change_group'):
        return HttpResponseForbidden()
    role = Role.objects.filter(pk=pk).first()

    permissions = [
        {'codename': 'change_recruitmentperiod', 'name': 'Administer recruitment', 'checked': False},
        {'codename': 'change_group', 'name': 'Administer roles', 'checked': False},
        {'codename': 'change_recruitmentapplication', 'name': 'Administer applications', 'checked': False},
    ]

    if role:
        for permission in permissions:
            for role_permission in role.rolepermission_set.all():
                if permission['codename'] == role_permission.permission.codename:
                    permission['checked'] = True

    if request.POST:
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
                role_permission = RolePermission()
                role_permission.permission = permission_object
                role_permission.role = role
                role_permission.save()
            else:
                RolePermission.objects.filter(permission=permission_object, role=role).delete()

        return redirect('/recruitment/')




    return render(request, template_name, {'role': role, 'permissions': permissions, 'roles': Role.objects.exclude(pk=role.pk) if role else Role.objects.all()})



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
        roles.append({'role': role, 'checked': len(RecruitableRole.objects.filter(recruitment_period=recruitment_period, role=role)) > 0})

    if form.is_valid():
        recruitment_period = form.save()
        for role in Role.objects.all():
            role_key = 'role_%d' % role.id
            if role_key in request.POST:
                if len(RecruitableRole.objects.filter(recruitment_period=recruitment_period, role=role)) == 0:
                    RecruitableRole.objects.create(recruitment_period=recruitment_period, role=role)
                print(role_key)
            else:
                RecruitableRole.objects.filter(recruitment_period=recruitment_period, role=role).delete()


        recruitment_period.interview_questions.handle_questions_from_request(request, 'interview_questions')
        recruitment_period.application_questions.handle_questions_from_request(request, 'application_questions')

        return redirect('/recruitment/%d' % recruitment_period.id)
    else:
        print(form.errors)
        print("Ai'nt no valid form!")


    return render(request, template_name, {
        'form': form,
        'roles': roles,
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


@login_required
def recruitment_application_new(request, recruitment_period_pk, pk=None, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)
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


    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()
    role_keys = [str(i) for i in range(recruitment_period.eligible_roles)]
    #role_ids = [int(request.POST[key]) for key in role_keys if key in request.POST and request.POST[key].isdigit()]

    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(request, request.user)
        if not recruitment_application:
            recruitment_application = RecruitmentApplication()

        recruitment_application.roleapplication_set.all().delete()

        recruitment_application.user = request.user
        recruitment_application.recruitment_period = recruitment_period
        recruitment_application.save()
        for role_number in range(recruitment_period.eligible_roles):
            if str(role_number) in request.POST and request.POST[str(role_number)].isdigit():
                role_id = int(request.POST[str(role_number)])
                role_application = RoleApplication()
                role_application.recruitment_application = recruitment_application
                role_application.recruitable_role = RecruitableRole.objects.filter(pk=role_id).first()
                role_application.order = role_number
                role_application.save()


        return redirect('/recruitment/%d' % recruitment_period.id)

    chosen_roles = [None for i in range(recruitment_period.eligible_roles)]

    if recruitment_application:
        role_applications = RoleApplication.objects.filter(recruitment_application=recruitment_application).order_by('order')

        for i in range(len(role_applications)):
            print(role_applications[i].recruitable_role, role_applications[i].order)
            chosen_roles[i] = role_applications[i].recruitable_role

    return render(request, template_name, {
        'application_questions_with_answers': recruitment_period.application_questions.questions_with_answers_for_user(recruitment_application.user if recruitment_application else None),
        'recruitment_period': recruitment_period,
        'chosen_roles': chosen_roles,
        'roles': RecruitableRole.objects.filter(recruitment_period=recruitment_period)
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
        except ValueError:
            setattr(model, model_field, None)
            model.save()



def recruitment_application_interview(request, pk, template_name='recruitment/recruitment_application_interview.html'):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not user_has_permission(request.user, 'change_recruitmentapplication') and application.interviewer != request.user:
        return HttpResponseForbidden()

    if request.POST:
        set_foreign_key_from_request(request, application, 'interviewer', User)
        set_foreign_key_from_request(request, application, 'recommended_role', Role)
        set_foreign_key_from_request(request, application, 'delegated_role', Role)
        set_foreign_key_from_request(request, application, 'superior_user', User)
        set_foreign_key_from_request(request, application, 'exhibitor', Company)
        set_int_key_from_request(request, application, 'rating')
        set_string_key_from_request(request, application, 'interview_location')
        set_string_key_from_request(request, application, 'interview_date')
        set_string_key_from_request(request, application, 'status')

        application.recruitment_period.interview_questions.handle_answers_from_request(request, application.user)
        application.recruitment_period.application_questions.handle_answers_from_request(request, application.user)

    exhibitors = [participation.company for participation in CompanyParticipationYear.objects.filter(fair=application.recruitment_period.fair)]


    class Status:
        def __init__(self, id):
            self.id = id

        def __str__(self):
            return self.id.capitalize() if self.id else 'None'


        def __eq__(self, other):
            return self.id == other.id



    return render(request, template_name, {
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(application.user),
        'interview_questions_with_answers': application.recruitment_period.interview_questions.questions_with_answers_for_user(application.user),
        'can_edit_recruitment_application': user_has_permission(request.user, 'change_recruitmentapplication'),
        'roles': [recruitable_role.role for recruitable_role in application.recruitment_period.recruitablerole_set.all()],
        'users': User.objects.all,
        'ratings': [i for i in range(1,6)],
        'exhibitors': exhibitors,
        'statuses': [Status(status[0]) for status in RecruitmentApplication.statuses],
        'selected_status': Status(application.status)

    })


def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not user_has_permission(request.user, 'recruitment.change_recruitmentapplication') and recruitment_application.user != request.user:
        return HttpResponseForbidden()
    recruitment_application.delete()
    return redirect('/recruitment/%d' % recruitment_application.recruitment_period.id)