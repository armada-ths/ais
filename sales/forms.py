from django.forms import ModelForm
from django.utils import timezone
from datetime import date
from django.template.defaultfilters import date as date_filter
from django.contrib.auth.models import User

import django.forms as forms

from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from fair.models import Fair
from lib.image import UploadToDirUUID

from .models import Sale
from register.models import SignupLog

class SalesSearchForm(forms.Form):
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    
    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    status = forms.ChoiceField(
        choices=[('', '---------')] + list(Sale.STATUS),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    contact_by_date = forms.ChoiceField(
        choices=[('', '---------'), ('TODAY', 'Today'), ('FUTURE', 'In the future'), ('PAST', 'In the past')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    diversity_room = forms.BooleanField(required = False)
    green_room = forms.BooleanField(required = False)
    events = forms.BooleanField(required = False)
    nova = forms.BooleanField(required = False)
    registered = forms.BooleanField(required = False)

    def sales_matching_search(self, sales_list, fair):
        search_form = self

        company = search_form.cleaned_data['company']
        if company:
            sales_list = [sale for sale in sales_list if company.lower() in sale.company.name.lower()]
        
        responsible = search_form.cleaned_data['responsible']
        if responsible:
            sales_list = [sale for sale in sales_list if responsible == sale.responsible]
        
        status = search_form.cleaned_data['status']
        if status:
            sales_list = [sale for sale in sales_list if status == sale.status]
        
        contact_by_date = search_form.cleaned_data['contact_by_date']
        if contact_by_date == 'TODAY':
            sales_list = [sale for sale in sales_list if sale.contact_by_date is not None and date.today() == sale.contact_by_date]
        elif contact_by_date == 'FUTURE':
            sales_list = [sale for sale in sales_list if sale.contact_by_date is not None and date.today() < sale.contact_by_date]
        elif contact_by_date == 'PAST':
            sales_list = [sale for sale in sales_list if sale.contact_by_date is not None and date.today() > sale.contact_by_date]
        
        diversity_room = search_form.cleaned_data['diversity_room']
        if diversity_room:
            sales_list = [sale for sale in sales_list if sale.diversity_room]
        
        green_room = search_form.cleaned_data['green_room']
        if green_room:
            sales_list = [sale for sale in sales_list if sale.green_room]
        
        events = search_form.cleaned_data['events']
        if events:
            sales_list = [sale for sale in sales_list if sale.events]
        
        nova = search_form.cleaned_data['nova']
        if nova:
            sales_list = [sale for sale in sales_list if sale.nova]
        
        registered = search_form.cleaned_data['registered']
        if registered:
            sales_list = [sale for sale in sales_list if sale.company in SignupLog.objects.filter(contract__fair=fair)]
        
        return sales_list
