from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.conf import settings
import json
import requests as r

from companies.models import Company, Contact

from exhibitors.models import Exhibitor
from fair.models import Fair
from sales.models import Sale
from .models import SignupContract, SignupLog

from .forms import CompanyForm, ContactForm, RegistrationForm, CreateContactForm, UserForm, InterestForm

def index(request, template_name='register/index.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is not None:
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:logout')
    return render(request, template_name)

def home(request, template_name='register/home.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is None:
            return redirect('anmalan:logout')
        else:
            ## Find what contact is signing in and the company
            fair = Fair.objects.get(current = True)
            registration_open = fair.registration_start_date <= timezone.now() and fair.registration_end_date > timezone.now()
            contract = SignupContract.objects.get(fair=fair, current=True)
            if registration_open:
                form1 = RegistrationForm(request.POST or None, prefix='registration')
                form2 = InterestForm(request.POST or None, prefix='interest')
                contact = Contact.objects.get(user=request.user)
                company = contact.belongs_to

                if form1.is_valid() and form2.is_valid():
                    SignupLog.objects.create(contact=contact, contract=contract, company = contact.belongs_to)
                    if len(Sale.objects.filter(fair=fair, company=company))==0:
                        sale = form2.save(commit=False)
                        sale.company = company
                        sale.save()
                    for sale in Sale.objects.filter(fair=fair, company=company):
                        sale.diversity_room = form2.cleaned_data['diversity_room']
                        sale.green_room = form2.cleaned_data['green_room']
                        sale.events = form2.cleaned_data['events']
                        sale.save()

                    r.post(settings.SALES_HOOK_URL,
                        data=json.dumps({'text': 'User {!s} just signed up {!s}!'.format(contact, company)}))

                    return redirect('anmalan:home')
                signed_up = SignupLog.objects.filter(company = company, contact=contact).first() != None
                return render(request, template_name, dict(registration_open = registration_open, 
                                                           signed_up = signed_up, 
                                                           contact = contact,
                                                           company=company, 
                                                           fair=fair,
                                                           form1=form1,
                                                           form2=form2,
                                                           contract_url=contract.contract.url))

           
            else:
                contact = Contact.objects.get(user=request.user)
                company = contact.belongs_to
                signed_up = SignupLog.objects.filter(company = company).first() != None
                    
                return render(request, template_name, dict(registration_open = registration_open, 
                                                           signed_up = signed_up, 
                                                           contact = contact,
                                                           company=company, 
                                                           fair=fair))
    return redirect('anmalan:index')



def signup(request, template_name='register/create_user.html'):
    contact_form = CreateContactForm(request.POST or None, prefix='contact')
    user_form = UserForm(request.POST or None, prefix='user')
    if contact_form.is_valid() and user_form.is_valid():
        user = user_form.save(commit=False)
        contact = contact_form.save(commit=False)
        user.username = contact.email
        user.email = contact.email
        user.save()
        contact.user = user
        contact.save()
        user = authenticate(username=contact_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password1'],
                                    )
        login(request, user)
        return redirect('anmalan:home')
    return render(request, template_name, dict(contact_form=contact_form, user_form=user_form))

def create_company(request, template_name='register/company_form.html'):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/register/signup')
    return render(request, template_name, dict(form=form))

def contact_update(request, template_name='register/contact_form.html'):
    contact = Contact.objects.get(user = request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        contact = form.save()
        return redirect('anmalan:home')
    return render(request, template_name, dict(form=form))

#update a company
def company_update(request, pk, template_name='register/company_form.html'):
    redirect_to = request.GET.get('next','')
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=company)
    if form.is_valid():
        form.save()
        if redirect_to:
            return redirect(redirect_to)
        return redirect('anmalan:home')
    return render(request, template_name, {'form':form})

   
