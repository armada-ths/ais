from django.shortcuts import render, redirect, get_object_or_404

from .models import RecruitmentPeriod, RecruitableRole, RecruitmentApplication, RoleApplication, InterviewQuestion, InterviewQuestionAnswer
from django.forms import ModelForm
from django import forms

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from django.forms import inlineformset_factory
from django.contrib.auth.models import Group, User
from django.forms import formset_factory

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
        }

class RecruitmentApplicationForm(ModelForm):
    class Meta:
        model = RecruitmentApplication
        fields = '__all__'

class RoleApplicationForm(ModelForm):

    def __init__(self, recruitment_period,*args,**kwargs):
        super (RoleApplicationForm,self ).__init__(*args,**kwargs)
        self.fields['recruitableRole'].queryset = RecruitableRole.objects.filter(recruitment_period=recruitment_period)

        for x in xrange(10):  # just a dummy for 10 values
            self.fields['col' + str(x)] = forms.CharField(label='Column ' + str(x), max_length=100, required=False)

    class Meta:
        model = RoleApplication
        fields = ('recruitableRole',)

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
    return redirect('recruitment')

def recruitment_period_new(request, template_name='recruitment/recruitment_period_new.html'):
    print("EY YO!")
    form = RecruitmentPeriodForm(request.POST or None)
    roles_form = inlineformset_factory(RecruitmentPeriod, RecruitableRole, fields=('role',))(request.POST or None)
    interview_questions_form = inlineformset_factory(RecruitmentPeriod, InterviewQuestion, fields=('recruitmentPeriod',))(request.POST or None)
    if form.is_valid() and roles_form.is_valid():
        recruitmentPeriod = form.save()
        roles_form.instance = recruitmentPeriod
        roles_form.save()
        return redirect('recruitment')
    else:
        print(form.errors)
        print("Ai'nt no valid form!")
    return render(request, template_name, {'form': form, 'roles_form': roles_form, 'interview_questions_form': interview_questions_form})



def recruitment_application_new(request, pk, template_name='recruitment/recruitment_application_new.html'):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    role_keys = ["1", "2", "3"]
    role_ids = [int(request.POST[key]) for key in role_keys if key in request.POST and request.POST[key].isdigit()]
    if len(role_ids) > 0:
        recruitment_application = RecruitmentApplication()
        recruitment_application.user = request.user
        recruitment_application.recruitmentPeriod = recruitment_period
        recruitment_application.save()
        for role_id in role_ids:
            role_application = RoleApplication()
            role_application.recruitmentApplication = recruitment_application
            role_application.recruitableRole = RecruitableRole.objects.filter(pk=role_id).first()
            role_application.save()
        return redirect('recruitment')


    return render(request, template_name, {
        'role_keys': role_keys,
        'roles': RecruitableRole.objects.filter(recruitment_period=recruitment_period)})


def set_foreign_key_from_request(request, model, model_field, foreign_key_model, request_key):
    if request_key in request.POST:
        try:
            foreign_key_id = int(request.POST[request_key])
            role = foreign_key_model.objects.filter(id=foreign_key_id).first()
            setattr(model, model_field, role)
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()

def set_int_key_from_request(request, model, model_field, request_key):
    if request_key in request.POST:
        try:
            setattr(model, model_field, int(request.POST[request_key]))
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()
            print('Role id was not an int')

def set_string_key_from_request(request, model, model_field, request_key):
    if request_key in request.POST:
        try:
            setattr(model, model_field, request.POST[request_key])
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()


def recruitment_application_interview(request, pk, template_name='recruitment/recruitment_application_interview.html'):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    print(request.POST)
    print(request.FILES)

    if request.POST:
        set_foreign_key_from_request(request, application, 'interviewer', User, 'interviewer')
        set_foreign_key_from_request(request, application, 'recommendedRole', RecruitableRole, 'recommended_role')
        set_foreign_key_from_request(request, application, 'delegatedRole', RecruitableRole, 'delegated_role')
        set_foreign_key_from_request(request, application, 'superiorUser', User, 'superior_user')
        set_int_key_from_request(request, application, 'rating', 'rating')
        set_string_key_from_request(request, application, 'interviewLocation', 'interviewLocation')
        set_string_key_from_request(request, application, 'interviewDate', 'interviewDate')

        for interviewQuestion in InterviewQuestion.objects.filter(recruitmentPeriod=application.recruitmentPeriod):
            key = '%s' % (interviewQuestion.id,)
            if interviewQuestion.fieldType == InterviewQuestion.FILE or interviewQuestion.fieldType == InterviewQuestion.IMAGE:
                if key in request.FILES:
                    file = request.FILES[key]
                    print("FOUND FILE")
                    print(request.FILES[key])
                    file_path = 'recruitment-applications/%d/%s' % (application.id, file.name,)
                    path = default_storage.save(file_path, ContentFile(file.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                    print(tmp_file)

                    answer, created = InterviewQuestionAnswer.objects.get_or_create(
                        interviewQuestion=interviewQuestion,
                        recruitmentApplication=application
                    )
                    answer.answer = file_path
                    answer.save()
            else:
                if key in request.POST:
                    print("FOUND %s - %s" % (key, request.POST[key]))
                    answer, created = InterviewQuestionAnswer.objects.get_or_create(
                        interviewQuestion=interviewQuestion,
                        recruitmentApplication=application
                    )
                    answer_string = request.POST[key]
                    print(key + " " + answer_string)

                    if answer_string:
                        answer.answer = answer_string
                        answer.save()

                else:
                    InterviewQuestionAnswer.objects.filter(
                            interviewQuestion=interviewQuestion,
                            recruitmentApplication=application
                        ).delete()

    interviewQuestions = []
    for interviewQuestion in InterviewQuestion.objects.all():
        answer = InterviewQuestionAnswer.objects.filter(interviewQuestion=interviewQuestion, recruitmentApplication=application).first()
        interviewQuestions.append((interviewQuestion, answer))

    return render(request, template_name, {
        'application': application,
        'field_type': {
            'check_box': InterviewQuestion.CHECK_BOX,
            'text_field': InterviewQuestion.TEXT_FIELD,
            'text_area': InterviewQuestion.TEXT_AREA,
            'radio_buttons': InterviewQuestion.RADIO_BUTTONS,
            'file': InterviewQuestion.FILE,
            'image': InterviewQuestion.IMAGE,
        },
        'interviewQuestions': interviewQuestions,
        'users': User.objects.all(),
        'roles': RecruitableRole.objects.filter(recruitment_period=application.recruitmentPeriod),
        'ratings': [i for i in range(1,6)],
    })


def recruitment_application_delete(request, pk):
    recruitmentApplication = get_object_or_404(RecruitmentApplication, pk=pk)
    recruitmentApplication.delete()
    return redirect('recruitment')