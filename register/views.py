from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings

from companies.models import Company, Contact
from orders.models import Product, Order
from exhibitors.models import Exhibitor
from fair.models import Fair
from sales.models import Sale
from matching.models import Survey

from .models import SignupContract, SignupLog

from .forms import EditCompanyForm, CompanyForm, ContactForm, RegistrationForm, CreateContactForm, CreateContactNoCompanyForm, UserForm, ExternalUserForm, ExternalUserLoginForm, InterestForm, ChangePasswordForm
from orders.forms import SelectStandAreaForm
from exhibitors.forms import ExhibitorProfileForm
from matching.forms import ResponseForm


from .help import exhibitor_form as help
from .help.methods import get_time_flag


def index(request, template_name='register/index.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is not None:
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:logout')
    timeFlag, [time_end, time_diff] = get_time_flag()
    fair = Fair.objects.filter(current=True).first()
    return render(request, template_name, {'fair': fair, 'timeFlag': timeFlag, 'time_end': time_end, 'time_diff': time_diff})

def preliminary_registration(request,fair, company, contact, contract, exhibitor, signed_up, profile_form, survey_form):
    form1 = RegistrationForm(request.POST or None, prefix='registration')
    form2 = InterestForm(request.POST or None, prefix='interest')
    form3 = SelectStandAreaForm(request.POST or None, prefix='stand_area')
    if not signed_up:
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            SignupLog.objects.create(contact=contact, contract=contract, company = contact.belongs_to)
            if len(Sale.objects.filter(fair=fair, company=company))==0:
                sale = form2.save(commit=False)
                sale.company = company
                sale.save()

            exhibitor = None
            try:
                exhibitor = Exhibitor.objects.get(company=company, fair=fair)
            except Exhibitor.DoesNotExist:
                # Try and copy exhibitor information from last year to make it easier to fill out the form.
                old_exhibitor = Exhibitor.objects.filter(company=company).order_by('-fair__year').first()
                exhibitor = None
                if old_exhibitor is None:
                    exhibitor = Exhibitor.objects.create(company=company, contact=contact, fair=fair, status='registered')
                else:
                    #Try to copy fields from last year. If failing, just create a new blank one
                    try:
                        exhibitor = create_new_exhibitor_from_old(old_exhibitor, contact, fair)
                    except:
                        exhibitor = Exhibitor.objects.create(company=company, contact=contact, fair=fair, status='registered')

            try:
                Order.objects.create(exhibitor=exhibitor, product=form3.cleaned_data['stand_area'], amount=1)
            except:
                pass

            for sale in Sale.objects.filter(fair=fair, company=company):
                sale.diversity_room = form2.cleaned_data['diversity_room']
                sale.green_room = form2.cleaned_data['green_room']
                sale.events = form2.cleaned_data['events']
                sale.nova = form2.cleaned_data['nova']
                sale.save()

            return redirect('anmalan:home')

    if profile_form.is_valid():
        profile_form.save()

    
    return render(request, 'register/registration.html', dict(registration_open = True,
                                               signed_up = signed_up,
                                               contact = contact,
                                               company=company,
                                               fair=fair,
                                               form1=form1,
                                               form2=form2,
                                               form3=form3,
                                               profile_form=profile_form,
                                               contract_url=contract.contract.url,
                                               survey_form=survey_form))


def complete_registration(request,fair, company, contact, contract, exhibitor, signed_up, profile_form, survey_form):
    form = help.create_exhibitor_form(request, fair, exhibitor, company, contact)

    # Only check survey form if there is a survey form
    if survey_form and  survey_form.is_valid():
        survey_form.save()
    else:
        print("survey_form invalid")

    if profile_form.is_valid():
        profile_form.save()
    else:
        print('profile_form invalid')

    if form.is_valid():
        # a huge amount of stuff happens here, check help/ExhibitorForm.py for details
        #help.save_exhibitor_form(request, form, currentFair, company, contact)
        pass

    print("signed_up:", signed_up)
    return render(request, 'register/registration.html', {'form': form, 'contract_url': contract.contract.url,
                                                              'signed_up': signed_up,
                                                              'company':company,
                                                              'contact':contact,
                                                              'complete_registration_open': True,
                                                              'fair':fair,
                                                              'profile_form': profile_form,
                                                              'survey_form': survey_form,
                                                              })



def home(request, template_name='register/registration.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is None:
            return redirect('anmalan:logout')
        else:
            ## Find what contact is signing in and the company
            fair = Fair.objects.get(current = True)
            pre_preliminary = fair.registration_start_date > timezone.now()
            registration_open = fair.registration_start_date <= timezone.now() and fair.registration_end_date > timezone.now()
            registration_closed = fair.registration_end_date < timezone.now()
            complete_registration_open = fair.complete_registration_start_date < timezone.now() and fair.complete_registration_close_date > timezone.now()
            complete_registration_closed = fair.complete_registration_close_date < timezone.now()

            contract = SignupContract.objects.get(fair=fair, current=True)
            contact = Contact.objects.get(user=request.user)
            company = contact.belongs_to
            exhibitor = Exhibitor.objects.filter(company=company, fair=fair).first()
            signed_up = SignupLog.objects.filter(company = company, contract=contract).first() != None

            profile_form = ExhibitorProfileForm(request.POST or None, prefix='exhibitor_profile', instance=exhibitor)
            current_matching_survey = Survey.objects.filter(fair=fair).first()
            survey_form = None
            if current_matching_survey:
                survey_form = ResponseForm(current_matching_survey, exhibitor, request.POST or None, prefix='matching')

            #needs to start check if complete is opened as that should override preliminary
            # There is a risk of having overlapping preliminary and complete registration dates. Therefore we need to check this.
            if complete_registration_open:
                if signed_up:
                    #return view of complete registration
                    return complete_registration(request,fair, company, contact, contract, exhibitor, signed_up, profile_form, survey_form=survey_form)

            if registration_open:
                return preliminary_registration(request,fair, company, contact, contract, exhibitor, signed_up, profile_form, survey_form=survey_form)

            if registration_closed:
                return render(request, template_name, dict(registration_closed = registration_closed,
                                                       signed_up = signed_up,
                                                       contact = contact,
                                                       company=company,
                                                       profile_form=profile_form,
                                                       fair=fair, survey_form=survey_form))
                #if signed_up:
                    #return view that says more information will come
                #    pass
                #else:
                #return view of that preliminary is closed and you are not signed up. Hope you come back next year.
                #    pass

            if pre_preliminary:
                # this should be basically nothing. Just return with variable, or return a specific template
                return render(request, template_name, dict(pre_preliminary = pre_preliminary,
                                                            contact=contact,
                                                            company=company,
                                                            fair=fair))


            if complete_registration_closed:
                if signed_up:
                    pass
                else:
                    pass


            return render(request, template_name, dict(registration_open = registration_open,
                                                       signed_up = signed_up,
                                                       contact = contact,
                                                       company=company,
                                                       fair=fair))
    return redirect('anmalan:index')


def create_new_exhibitor_from_old(old_exhibitor, contact, fair):
    exhibitor = Exhibitor.objects.create(fair=fair, status='registered',
            company=old_exhibitor.company,
            contact=contact,
            about_text = old_exhibitor.about_text,
            logo = old_exhibitor.logo,
            requests_for_stand_placement = old_exhibitor.requests_for_stand_placement,
            other_information_about_the_stand = old_exhibitor.other_information_about_the_stand,
            invoice_reference = old_exhibitor.invoice_reference,
            invoice_purchase_order_number = old_exhibitor.invoice_purchase_order_number,
            invoice_reference_phone_number = old_exhibitor.invoice_reference_phone_number,
            invoice_organisation_name = old_exhibitor.invoice_organisation_name,
            invoice_address = old_exhibitor.invoice_address,
            invoice_address_po_box = old_exhibitor.invoice_address_po_box,
            invoice_address_zip_code = old_exhibitor.invoice_address_zip_code,
            invoice_identification = old_exhibitor.invoice_identification,
            invoice_additional_information = old_exhibitor.invoice_additional_information
            )
    # ManyToMany fields needs to be copied after creation
    # the * unpacks the list, taking [a,b,c] to a,b,c
    exhibitor.job_types.add(*old_exhibitor.job_types.all())
    exhibitor.save()
    return exhibitor








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

def external_signup(request, template_name='register/create_external_user.html'):
    """
    Sign up for external people meaning those who are not in Armada and not from KTH.
    """
    fair = get_object_or_404(Fair, current=True)
    if request.user.is_authenticated():
        # TODO: this line needs to be changed for next years banquet signup.
        # Now it redirects to placement
        return HttpResponseRedirect(reverse('banquet/placement', kwargs={'year': fair.year}))
    else:
        form = ExternalUserForm(request.POST or None, prefix='user')
        if form.is_valid():
            user = form.save(commit=False)
            mail = form.cleaned_data['email'].lower()
            user.username = mail
            user.email = mail
            # the form's cleaning checks if the user email already exists
            user.save()
            user = authenticate(
                username=mail,
                password=form.cleaned_data['password1'],
            )
            login(request, user)

            return HttpResponseRedirect(reverse('banquet/signup', kwargs={'year': fair.year}))
    return render(request, template_name, dict(form=form, year=fair.year))

def external_login(request, template_name='register/external_login.html'):
    """
    Login in for external people meaning those who are not in Armada and not from KTH.
    Will redirect to external banquet signup
    """
    form = ExternalUserLoginForm(request.POST or None)
    fair = get_object_or_404(Fair, current=True)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data['email'].lower(),
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('banquet/placement', kwargs={'year': fair.year}))

    return render(request, template_name, dict(form=form, year=fair.year))

def create_company(request, template_name='register/company_form.html'):
    form = CompanyForm(request.POST or None)
    contact_form = CreateContactNoCompanyForm(request.POST or None, prefix='contact')
    user_form = UserForm(request.POST or None, prefix='user')
    if contact_form.is_valid() and user_form.is_valid() and form.is_valid():
        company = form.save()
        user = user_form.save(commit=False)
        contact = contact_form.save(commit=False)
        user.username = contact.email
        user.email = contact.email
        user.save()
        contact.user = user
        contact.confirmed = True #Auto confirm contacts who register a new company
        contact.belongs_to = company
        contact.save()
        user = authenticate(username=contact_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password1'],
                                    )
        login(request, user)
        return redirect('anmalan:home')
    return render(request, template_name, dict(form=form, contact_form=contact_form, user_form=user_form))


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
    form = EditCompanyForm(request.POST or None, instance=company)
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
