from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, CustomField, CustomFieldAnswer, CustomFieldArgument
from django.forms import ModelForm
from django import forms

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from django.contrib.auth.models import Group, User

import os


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

class RecruitmentApplicationForm(ModelForm):
    class Meta:
        model = RecruitmentApplication
        fields = '__all__'

class RoleApplicationForm(ModelForm):

    def __init__(self, recruitment_period,*args,**kwargs):
        super (RoleApplicationForm,self ).__init__(*args,**kwargs)
        self.fields['recruitable_role'].queryset = RecruitableRole.objects.filter(recruitment_period=recruitment_period)

        for x in xrange(10):  # just a dummy for 10 values
            self.fields['col' + str(x)] = forms.CharField(label='Column ' + str(x), max_length=100, required=False)

    class Meta:
        model = RoleApplication
        fields = ('recruitable_role',)

def recruitment(request, template_name='recruitment/recruitment.html'):
    recruitmentPeriods = RecruitmentPeriod.objects.all()
    data = {}
    data['recruitment_periods'] = recruitmentPeriods
    return render(request, template_name, data)

def recruitment_period(request, pk, template_name='recruitment/recruitment_period.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    data = {}
    data['period'] = recruitment_period
    return render(request, template_name, data)

def recruitment_period_delete(request, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    recruitment_period.delete()
    return redirect('/recruitment/')


def recruitment_period_edit(request, pk=None, template_name='recruitment/recruitment_period_new.html'):
    recruitment_period = RecruitmentPeriod.objects.filter(pk=pk).first()
    form = RecruitmentPeriodForm(request.POST or None, instance=recruitment_period)
    roles = []

    for role in Group.objects.filter(is_role=True):
        roles.append({'role': role, 'checked': len(RecruitableRole.objects.filter(recruitment_period=recruitment_period, role=role)) > 0})

    #('application_question', [], recruitment_period.application_questions, []),

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

        extra_fields = [('question', [], recruitment_period.extra_field, []), ('application_questions', [], recruitment_period.application_questions, [])]

        for extra_field in extra_fields:

            question_ids = extra_field[1]
            print("EXTRA_FIELD: " + extra_field[0])
            for key in request.POST:
                question_key_prefix = extra_field[0] + '_'
                key_split = key.split(question_key_prefix)
                if len(key_split) == 2:
                    question_ids.append(int(key_split[1]))

            for question in extra_field[2].customfield_set.all():
                print(question)
                if question.id not in question_ids:
                    question.delete()

            for question_id in question_ids:
                custom_field = CustomField.objects.filter(pk=question_id).first()
                if not custom_field:
                    custom_field = CustomField()

                custom_field.extra_field = extra_field[2]
                custom_field.question = request.POST['%s_%d' % (extra_field[0], question_id)]
                custom_field.field_type = request.POST['%s-type_%d' % (extra_field[0], question_id)]
                custom_field.save()

                print('Storing custom field %d' % question_id)
                print('Field type %s' % custom_field.field_type)
                print('Extra Field type %s' % custom_field.extra_field.id)
                print('Question %s' % custom_field.question)

                for argument in custom_field.customfieldargument_set.all():
                    if 'argument_%d_%d' % (question_id, argument.id) not in request.POST:
                        argument.delete()

                for key in request.POST:
                    argument_key_prefix = 'argument_%d_' % question_id
                    key_split = key.split(argument_key_prefix)
                    if len(key_split) == 2:
                        print(key)
                        print(key_split)
                        argument_id = int(key_split[1])
                        argument_key = 'argument_%d_%d' % (question_id, argument_id)

                        custom_field_argument = CustomFieldArgument.objects.filter(pk=argument_id).first()
                        if not custom_field_argument:
                            custom_field_argument = CustomFieldArgument()

                        custom_field_argument.custom_field = custom_field
                        custom_field_argument.value = request.POST[argument_key]
                        custom_field_argument.save()

        return redirect('/recruitment/%d' % recruitment_period.id)
    else:
        print(form.errors)
        print("Ai'nt no valid form!")

    custom_fields = {'question': [], 'application_questions': []}
    custom_field_ids = {'question': [], 'application_questions': []}
    if recruitment_period:
        extra_fields = [('question', [], recruitment_period.extra_field, []),
                        ('application_questions', [], recruitment_period.application_questions, [])]
        for extra_field in extra_fields:
            for question in extra_field[2].customfield_set.all():
                #custom_fields[]
                custom_fields[extra_field[0]].append(question)
                custom_field_ids[extra_field[0]].append(question.id)
                #extra_field[3].append(question)


    #return render(request, template_name, {'form': form, 'roles': roles, 'fields': CustomField.fields, 'custom_fields': custom_fields, 'custom_field_ids': map(lambda x: x.id, custom_fields)})
    return render(request, template_name, {'form': form, 'roles': roles, 'fields': CustomField.fields,
                                                       'custom_fields': custom_fields,
                                                       'custom_field_ids': custom_field_ids})


def recruitment_application_new(request, pk, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    role_keys = [str(i) for i in range(0, recruitment_period.eligible_roles)]
    role_ids = [int(request.POST[key]) for key in role_keys if key in request.POST and request.POST[key].isdigit()]



    handleCustomFieldsFromRequest(request, recruitment_period.application_questions)

    custom_fields = []
    for custom_field in recruitment_period.application_questions.customfield_set.all():
        answer = CustomFieldAnswer.objects.filter(custom_field=custom_field,
                                                            user=request.user).first()
        custom_fields.append((custom_field, answer))

    if len(role_ids) > 0:
        recruitment_application = RecruitmentApplication()
        recruitment_application.user = request.user
        recruitment_application.recruitment_period = recruitment_period
        recruitment_application.save()
        for role_id in role_ids:
            role_application = RoleApplication()
            role_application.recruitment_application = recruitment_application
            role_application.recruitable_role = RecruitableRole.objects.filter(pk=role_id).first()
            role_application.save()
        return redirect('/recruitment/%d' % recruitment_period.id)


    print(recruitment_period.application_questions.questions_with_answers_for_user(request.user))

    return render(request, template_name, {
        'application_questions': recruitment_period.application_questions.questions_with_answers_for_user(request.user),
        'recruitment_period': recruitment_period,
        'custom_fields': custom_fields,
        'role_keys': role_keys,
        'roles': RecruitableRole.objects.filter(recruitment_period=recruitment_period)})


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


def handleCustomFieldsFromRequest(request, extra_field):
    print(request.FILES)
    print("Number of extra fields: %d" % len(extra_field.customfield_set.all()))

    for custom_field in extra_field.customfield_set.all():
        key = '%s' % (custom_field.id,)
        print('looking for key: %s' % key)
        if custom_field.field_type == 'file' or custom_field.field_type == 'image':
            print("looking for %s" % custom_field.field_type)
            if key in request.FILES:
                file = request.FILES[key]
                print(request.FILES[key])
                file_path = 'custom-field/%d_%s.%s' % (request.user.id, key, file.name.split('.')[-1])
                path = default_storage.save(file_path, ContentFile(file.read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                print(tmp_file)

                answer, created = CustomFieldAnswer.objects.get_or_create(
                    custom_field=custom_field,
                    user=request.user
                )
                answer.answer = file_path
                answer.save()
        else:
            if key in request.POST:
                print("FOUND %s - %s" % (key, request.POST[key]))
                answer, created = CustomFieldAnswer.objects.get_or_create(
                    custom_field=custom_field,
                    user=request.user
                )
                answer_string = request.POST[key]
                print(key + " " + answer_string)

                if answer_string:
                    answer.answer = answer_string
                    answer.save()

            else:
                CustomFieldAnswer.objects.filter(
                    custom_field=custom_field,
                    user=request.user
                ).delete()

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
        handleCustomFieldsFromRequest(request, application.recruitment_period.extra_field)
        handleCustomFieldsFromRequest(request, application.recruitment_period.application_questions)


    custom_field_sections = []

    interviewQuestions = []
    for custom_field in application.recruitment_period.extra_field.customfield_set.all():
        answer = CustomFieldAnswer.objects.filter(custom_field=custom_field,
                                                            user=request.user).first()
        interviewQuestions.append((custom_field, answer))

    custom_field_sections.append({'section_name': 'Interview questions', 'custom_fields': interviewQuestions})

    applicationQuestions = []
    for custom_field in application.recruitment_period.application_questions.customfield_set.all():
        answer = CustomFieldAnswer.objects.filter(custom_field=custom_field,
                                                  user=request.user).first()
        applicationQuestions.append((custom_field, answer))
    custom_field_sections.append({'section_name': 'Application questions', 'custom_fields': applicationQuestions})


    return render(request, template_name, {
        'application': application,
        'application_questions': application.recruitment_period.application_questions.questions_with_answers_for_user(request.user),
        'interview_questions': application.recruitment_period.extra_field.questions_with_answers_for_user(request.user),
        'custom_field_sections': custom_field_sections,
        'users': User.objects.all(),
        'roles': RecruitableRole.objects.filter(recruitment_period=application.recruitment_period),
        'ratings': [i for i in range(1,6)]
    })


def recruitment_application_delete(request, pk):
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    recruitment_application.delete()
    return redirect('/recruitment/%d' % recruitment_application.recruitment_period.id)