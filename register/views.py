from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings

from companies.models import Company, Contact
from orders.models import Product, Order
from exhibitors.models import Exhibitor
from fair.models import Fair
from sales.models import Sale

from .models import SignupContract, SignupLog
from .forms import CompanyForm, ContactForm, RegistrationForm, CreateContactForm, UserForm, InterestForm, ChangePasswordForm

from .help import exhibitor_form as help
from .help.methods import get_time_flag

def index(request, template_name='register/index.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is not None:
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:logout')
    timeFlag, [time_end, time_diff] = get_time_flag()
    return render(request, template_name, {'timeFlag': timeFlag, 'time_end': time_end, 'time_diff': time_diff})

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
                        sale.nova = form2.cleaned_data['nova']
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

# A company's contact can request to have the company
# become an exhibitor via the ExhibitorForm
def create_exhibitor(request, template_name='register/exhibitor_form.html'):
    """
    Complete Registration: create_exhibitor view
    ===============
    The complete registration is where already signed up companies with contacts
    can make their final selection of products and send in important info such as
    invoice address ('faktura' in SWE). The view create_exhibitor() creates the
    ExhibitorForm, gets the answers and updates the DB.

    Steps
    ----------------
    Here is the main steps of what this view does:

     * Check that the current user has a connected company with a contact
     * Check if the company already is an exhibitor or not
     * Get all products from DB and also eventual current Orders if the company already is an exhibitor
     * Initilaze the form and wait for the POST request from user submission
     * Find all selected products and update DB accordingly.
     * Update or create exhibitor from the fields entered in form
     * Update company and contact info (some field in the form helps the user update the company's
     info incase they want any last minute changes)
     * Create a log of a contract being signed for the current company becoming an exhibitor

     Extra Info
     ----------------
     * If the user 'saves' then the DB will be updated. If one 'submits' then a
     confirmation email will be sent out.
     * 'Bool products' are products that has checkboxes, e.g do you want the x room?
     * 'Amount products' are products chosen in an amount, e.g amoutn of banquet tickets.


     """

    currentFair = Fair.objects.get(current = True)
    # Return 404 if no contract.
    # if no contact or company connected to
    # user then redirect to logout
    contract = get_object_or_404(SignupContract, fair=currentFair, current=True)

    if request.user.is_authenticated():
        contact = Contact.objects.get(user=request.user)
        # make sure user is connected to a 'Contact'
        if contact is None:
            return redirect('anmalan:logout')
        else:
            # make sure a 'Company' is connected to contact
            company = contact.belongs_to
            if company is None:
                return redirect('anmalan:logout')

            exhibitor = None
            try:
                exhibitor = Exhibitor.objects.get(company=company, fair=currentFair)
            except Exhibitor.DoesNotExist:
                pass

            form = help.create_exhibitor_form(request, currentFair, exhibitor, company, contact)

            if form.is_valid():
                # a huge amount of stuff happens here, check help/ExhibitorForm.py for details
                help.save_exhibitor_form(request, form, currentFair, company, contact)

    return render(request, template_name, {'form': form, 'contract_url': contract.contract.url})


# thank you screen after submission of complete registration
def cr_done(request, template_name='register/finished_registration.html'):
    return render(request, template_name)


#change password
def change_password(request, template_name='register/change_password.html'):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:change_password')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, template_name, {'form':form})
