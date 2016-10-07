from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from companies.models import Company, Contact

###COMPANY###
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

#list all companies
def companies_list(request, template_name='companies/companies_list.html'):
    companies = Company.objects.all()
    data = {}
    data['object_list'] = companies
    return render(request, template_name, data)

#list one company
def list_company(request, pk, template_name='companies/list_company.html'):
    company = get_object_or_404(Company, pk=pk)
    return render(request, template_name, {'company':company})

#crate a company
def company_create(request, template_name='companies/company_form.html'):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('companies_list')
    return render(request, template_name, {'form':form})

#update a company
def company_update(request, pk, template_name='companies/company_form.html'):
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=company)
    if form.is_valid():
        form.save()
        return redirect('companies_list')
    return render(request, template_name, {'form':form})

#delete a company
def company_delete(request, pk, template_name='companies/company_confirm_delete.html'):
    company = get_object_or_404(Company, pk=pk)
    if request.method=='POST':
        company.delete()
        return redirect('companies_list') #redirect back to company list
    return render(request, template_name, {'object':company})

###COMPANY CONTACT###
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

#crate a company contact
def contact_create(request, pk, template_name='companies/contact_form.html'):
    form = ContactForm(request.POST or None)
    company = get_object_or_404(Company, pk=pk)
    if form.is_valid():
        form.save()
        return render(request, template_name, {'company':company})
    return render(request, template_name, {'form':form})
