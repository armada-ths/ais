from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from companies.models import Company, Contact
from fair.models import Fair


###COMPANY###
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

def current_fair():
    return get_object_or_404(Fair, year=2017)

#list all companies
def companies_list(request, template_name='companies/companies_list.html'):
    fair = current_fair()
    companies = Company.objects.all()
    return render(request, template_name, dict(object_list=companies, fair=fair))

#list one company
def list_company(request, pk, template_name='companies/list_company.html'):
    fair = current_fair()
    company = get_object_or_404(Company, pk=pk)
    return render(request, template_name, {'company':company, 'fair':fair})

#crate a company
def company_create(request, template_name='companies/company_form.html'):
    fair = current_fair()
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('companies_list')
    return render(request, template_name, {'form':form, 'fair':fair})

#update a company
def company_update(request, pk, template_name='companies/company_form.html'):
    redirect_to = request.GET.get('next','')
    fair = current_fair()
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=company)
    if form.is_valid():
        form.save()
        if redirect_to:
            return redirect(redirect_to)
        return redirect('companies_list')
    return render(request, template_name, {'form':form, 'fair':fair})

#delete a company
def company_delete(request, pk, template_name='companies/company_confirm_delete.html'):
    fair = current_fair()
    company = get_object_or_404(Company, pk=pk)
    if request.method=='POST':
        company.delete()
        return redirect('companies_list') #redirect back to company list
    return render(request, template_name, {'object':company, 'fair':fair})

###COMPANY CONTACT###
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user',)

#crate a company contact
def contact_create(request, pk, template_name='companies/contact_form.html'):
    redirect_to = request.GET.get('next','')
    fair = current_fair()
    form = ContactForm(request.POST or None)
    company = get_object_or_404(Company, pk=pk)
    if form.is_valid():
        form.save()
        if redirect_to:
            return redirect(redirect_to)
        return render(request, template_name, {'company':company, 'fair':fair})
    return render(request, template_name, {'form':form, 'fair':fair})

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

def contact_state_toggle(request, contact_pk, template_name='companies/user_form.html'):
    redirect_to = request.GET.get('next','')
    fair = current_fair()
    contact = get_object_or_404(Contact, pk=contact_pk)
    if contact.active:
        contact.active = False
        
    else:
        if not contact.user:
            form = UserForm(request.POST or None)   
            print(form)
            if not form.is_valid():
                return render(request, template_name, {'form':form, 'fair':fair})
            user = form.save(commit=False)
            user.username = contact.email
            user.email = contact.email
            user.save()
            contact.user = user
        contact.active = True
    contact.save()
    return redirect(redirect_to)


