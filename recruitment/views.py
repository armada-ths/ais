from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test


def user_is_pg(user):
    return user.groups.filter(name='PG').exists()


class RecruitmentPeriodForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecruitmentPeriodForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RecruitmentPeriod
        fields = '__all__'

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "extra_field": forms.HiddenInput(),
            "application_questions": forms.HiddenInput(),
        }


@user_passes_test(user_is_pg)
def recruitment(request, template_name='recruitment/recruitment.html'):
    recruitmentPeriods = RecruitmentPeriod.objects.all()
    data = {}
    data['recruitment_periods'] = recruitmentPeriods
    return render(request, template_name, data)


@user_passes_test(user_is_pg)
def recruitment_period(request, pk, template_name='recruitment/recruitment_period.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    data = {}
    data['recruitment_period'] = recruitment_period
    return render(request, template_name, data)


@user_passes_test(user_is_pg)
def recruitment_period_delete(request, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    recruitment_period.delete()
    return redirect('/recruitment/')


@user_passes_test(user_is_pg)
def recruitment_period_edit(request, pk=None, template_name='recruitment/recruitment_period_new.html'):
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


        recruitment_period.extra_field.handle_questions_from_request(request, 'extra_field')
        recruitment_period.application_questions.handle_questions_from_request(request, 'application_questions')

        return redirect('/recruitment/%d' % recruitment_period.id)
    else:
        print(form.errors)
        print("Ai'nt no valid form!")


    return render(request, template_name, {
        'form': form,
        'roles': roles,
        'extra_field': [] if not recruitment_period else recruitment_period.extra_field.customfield_set.all(),
        'application_questions': [] if not recruitment_period else recruitment_period.application_questions.customfield_set.all(),
    })


@user_passes_test(user_is_pg)
def recruitment_application_new(request, recruitment_period_pk, pk=None, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)
    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()
    role_keys = [str(i) for i in range(0, recruitment_period.eligible_roles)]
    role_ids = [int(request.POST[key]) for key in role_keys if key in request.POST and request.POST[key].isdigit()]

    if len(role_ids) > 0:
        recruitment_period.application_questions.handle_answers_from_request(request)
        if not recruitment_application:
            recruitment_application = RecruitmentApplication()

        recruitment_application.roleapplication_set.all().delete()

        recruitment_application.user = request.user
        recruitment_application.recruitment_period = recruitment_period
        recruitment_application.save()
        for role_id in role_ids:
            role_application = RoleApplication()
            role_application.recruitment_application = recruitment_application
            role_application.recruitable_role = RecruitableRole.objects.filter(pk=role_id).first()
            role_application.save()
        return redirect('/recruitment/%d' % recruitment_period.id)

    chosen_roles = [None for i in range(recruitment_period.eligible_roles)]

    if recruitment_application:
        role_applications = RoleApplication.objects.filter(recruitment_application=recruitment_application)
        for i in range(len(role_applications)):
            chosen_roles[i] = role_applications[i].recruitable_role

    return render(request, template_name, {
        'application_questions_with_answers': recruitment_period.application_questions.questions_with_answers_for_user(request.user),
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


@user_passes_test(user_is_pg)
def recruitment_application_interview(request, pk, template_name='recruitment/recruitment_application_interview.html'):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    print(request.POST)
    print(request.FILES)

    if request.POST:
        set_foreign_key_from_request(request, application, 'interviewer', User)
        set_foreign_key_from_request(request, application, 'recommended_role', RecruitableRole)
        set_foreign_key_from_request(request, application, 'delegated_role', RecruitableRole)
        set_foreign_key_from_request(request, application, 'superior_user', User)
        set_int_key_from_request(request, application, 'rating')
        set_string_key_from_request(request, application, 'interview_location')
        set_string_key_from_request(request, application, 'interview_date')

        application.recruitment_period.extra_field.handle_answers_from_request(request)
        application.recruitment_period.application_questions.handle_answers_from_request(request)

    return render(request, template_name, {
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(request.user),
        'interview_questions_with_answers': application.recruitment_period.extra_field.questions_with_answers_for_user(request.user),
        'roles': RecruitableRole.objects.filter(recruitment_period=application.recruitment_period),
        'ratings': [i for i in range(1,6)]
    })


@user_passes_test(user_is_pg)
def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    recruitment_application.delete()
    return redirect('/recruitment/%d' % recruitment_application.recruitment_period.id)