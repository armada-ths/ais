from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from companies.models import Company, CompanyContact

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

def server_list(request, template_name='servers/server_list.html'):
    servers = Company.objects.all()
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)