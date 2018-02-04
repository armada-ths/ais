from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from companies.models import Company, Contact, InvoiceDetails
from fair.models import Fair
from .forms import CompanyForm, ContactForm, UserForm


def current_fair():
    return get_object_or_404(Fair, current=True)

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
# By keeping raise_exception=False, any user who tries to access this 
# page gets logged out. If set to True, it crashes as fair.year does not 
# necessarily exists and then base.html cannot load.
# TODO: This is bad design which might need fixing
@permission_required('companies.company.can_add_company', raise_exception=False)
def company_create(request, template_name='companies/company_form.html'):
    fair = current_fair()
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        next = request.GET.get('next')
        if next:
            return redirect(next)
        #return redirect('companies:companies_list') #Do not support accessing this separate
    return render(request, template_name, {'form':form, 'fair':fair})

#update a company
@permission_required('companies.company.can_change_company', raise_exception=False)
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
@permission_required('companies.company.can_delete_company', raise_exception=False)
def company_delete(request, pk, template_name='companies/company_confirm_delete.html'):
    fair = current_fair()
    company = get_object_or_404(Company, pk=pk)
    if request.method=='POST':
        company.delete()
        return redirect('companies_list') #redirect back to company list
    return render(request, template_name, {'object':company, 'fair':fair})


#crate a company contact
def contact_create(request, pk, template_name='companies/contact_form.html'):
    redirect_to = request.GET.get('next','')
    fair = current_fair()
    contact_form = ContactForm(request.POST or None, prefix='contact')
    user_form = UserForm(request.POST or None, prefix='user')
    company = get_object_or_404(Company, pk=pk)

    if contact_form.is_valid() and user_form.is_valid():
        user = user_form.save(commit=False)
        contact = contact_form.save(commit=False)
        contact.email = contact.email.lower() #The username is converted to lowecase when used in the login-form
        
        user.username = contact.email
        user.email = contact.email
        user.save()
        contact.user = user
        contact.save()

        if redirect_to:
            return redirect(redirect_to)
        return render(request, template_name, {'company':company, 'fair':fair})
    return render(request, template_name, {'contact_form':contact_form, 'user_form':user_form, 'fair':fair})


def contact_active_toggle(request, contact_pk, template_name='companies/user_form.html'):
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

def contact_confirm_toggle(request, contact_pk):
    redirect_to = request.GET.get('next','')
    fair = current_fair()
    contact = get_object_or_404(Contact, pk=contact_pk)
    if contact.confirmed:
        contact.confirmed = False
    else:
        contact.confirmed = True
    contact.save()
    return redirect(redirect_to)



