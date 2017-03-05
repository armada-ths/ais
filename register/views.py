from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.forms import ModelForm, Form, BooleanField
from django.utils import timezone

from companies.models import Company, Contact

from exhibitors.models import Exhibitor
from fair.models import Fair
from .models import SignupContract, SignupLog

###COMPANY###
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class RegistrationForm(Form):
    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the contract and agree to terms"

def home(request, template_name='register/home.html'):
    company = Company.objects.all().first()
    return render(request, template_name, dict(company=company))
    
def fair(request, template_name='register/fair.html'):
    fair  = get_object_or_404(Fair, year=2017)
    registration_open = fair.registration_start_date <= timezone.now() and fair.registration_end_date > timezone.now()
    return render(request, template_name, dict(fair=fair, registration_open = registration_open))

def prel_registration(request, fair_id, template_name='register/prel_registration.html'):
    fair = get_object_or_404(Fair, id=fair_id)
    registration_open = fair.registration_start_date <= timezone.now() and fair.registration_end_date > timezone.now()
    contract = SignupContract.objects.get(fair=fair, current=True)
    if registration_open:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            contact = Contact.objects.get(user=request.user)
            status = dict(Exhibitor.statuses)['registered']
            exhibitor = Exhibitor.objects.create(fair=fair, company=contact.belongs_to, contact=contact, status=status)
            SignupLog.objects.create(contact=contact, contract=contract)
            return redirect('/register')
        return render(request, template_name, {'form':form, 'contract_url':contract.contract.url})
            
    else:
        return HttpResponse("Sorry, registration is closed!")
    
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

   
