from django.shortcuts import render

from .models import RecruitmentPeriod

# Create your views here.
#list all companies
def recruitment(request, template_name='recruitment/recruitment.html'):
    recruitmentPeriods = RecruitmentPeriod.objects.all()
    data = {}
    data['recruitment_periods'] = recruitmentPeriods
    return render(request, template_name, data)
