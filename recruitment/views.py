from django.shortcuts import render, redirect

from .models import RecruitmentPeriod, RecruitableRole
from django.forms import ModelForm
from django import forms

from django.forms import inlineformset_factory

class RecruitmentPeriodForm(ModelForm):
    class Meta:
        model = RecruitmentPeriod
        fields = '__all__'

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }

        inlines = [
            RecruitableRole
        ]


def recruitment(request, template_name='recruitment/recruitment.html'):
    recruitmentPeriods = RecruitmentPeriod.objects.all()
    data = {}
    data['recruitment_periods'] = recruitmentPeriods
    return render(request, template_name, data)

def recruitment_period_new(request, template_name='recruitment/recruitment_period_new.html'):
    print("EY YO!")
    form = RecruitmentPeriodForm(request.POST or None)
    roles_form = inlineformset_factory(RecruitmentPeriod, RecruitableRole, fields=('role',))(request.POST or None)
    if form.is_valid() and roles_form.is_valid():
        recruitmentPeriod = form.save()
        roles_form.instance = recruitmentPeriod
        roles_form.save()
        return redirect('recruitment')
    else:
        print(form.errors)
        print("Ai'nt no valid form!")
    return render(request, template_name, {'form': form, 'roles_form': roles_form})
