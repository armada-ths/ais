from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def user_has_permission(user, needed_permission):
    if user.has_perm(needed_permission):
        return True
    for application in RecruitmentApplication.objects.filter(user=user, status='accepted'):
        for permission in application.delegated_role.role.permissions.all():

            print(permission.codename)
            if permission.codename == needed_permission:
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

class RoleForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name','permissions']


def recruitment(request, template_name='recruitment/recruitment.html'):
    return render(request, template_name, {
        'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
        'roles': Group.objects.filter(is_role=True),
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
    role = Group.objects.filter(pk=pk).first()

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

    if request.POST:
        if not role:
            role = Group()
        role.name = request.POST['name']
        role.is_role = True
        role.save()

        for permission in permissions:
            codename = permission['codename']
            permission_object = Permission.objects.get(codename=permission['codename'])
            if codename in request.POST:
                role.permissions.add(permission_object)
            else:
                role.permissions.remove(permission_object)

        return redirect('/recruitment/')




    return render(request, template_name, {'role': role, 'permissions': permissions})



def roles_delete(request, pk):
    role = get_object_or_404(Group, pk=pk)
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

    for role in Group.objects.filter(is_role=True):
        roles.append({'role': role, 'checked': len(RecruitableRole.objects.filter(recruitment_period=recruitment_period, role=role)) > 0})

    if form.is_valid():
        recruitment_period = form.save()
        for role in Group.objects.filter(is_role=True):
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
    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()
    role_keys = [str(i) for i in range(recruitment_period.eligible_roles)]
    #role_ids = [int(request.POST[key]) for key in role_keys if key in request.POST and request.POST[key].isdigit()]

    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(request)
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
        set_foreign_key_from_request(request, application, 'recommended_role', RecruitableRole)
        set_foreign_key_from_request(request, application, 'delegated_role', RecruitableRole)
        set_foreign_key_from_request(request, application, 'superior_user', User)
        set_int_key_from_request(request, application, 'rating')
        set_string_key_from_request(request, application, 'interview_location')
        set_string_key_from_request(request, application, 'interview_date')
        set_string_key_from_request(request, application, 'status')

        application.recruitment_period.interview_questions.handle_answers_from_request(request)
        application.recruitment_period.application_questions.handle_answers_from_request(request)

    return render(request, template_name, {
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(application.user),
        'interview_questions_with_answers': application.recruitment_period.interview_questions.questions_with_answers_for_user(request.user),
        'can_edit_recruitment_application': user_has_permission(request.user, 'change_recruitmentapplication'),
        'roles': RecruitableRole.objects.filter(recruitment_period=application.recruitment_period),
        'users': User.objects.all,
        'ratings': [i for i in range(1,6)]
    })


def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    if not user_has_permission(request.user, 'recruitment.change_recruitmentapplication') and recruitment_application.user != request.user:
        return HttpResponseForbidden()
    recruitment_application.delete()
    return redirect('/recruitment/%d' % recruitment_application.recruitment_period.id)