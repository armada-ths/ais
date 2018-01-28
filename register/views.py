from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings

import requests as r

from companies.models import Company, Contact, InvoiceDetails
from orders.models import Product, Order, ProductType, ElectricityOrder
from exhibitors.models import Exhibitor, TransportationAlternative
from fair.models import Fair
from sales.models import Sale
from matching.models import Survey

from .models import SignupContract, SignupLog, OrderLog

from .forms import  RegistrationForm,  InterestForm, ChangePasswordForm
from orders.forms import SelectStandAreaForm, get_order_forms, ElectricityOrderForm
from exhibitors.forms import ExhibitorProfileForm, SelectInvoiceDetailsForm, TransportationForm
from matching.forms import ResponseForm
from companies.forms import InvoiceDetailsForm, CompanyForm, ContactForm, EditCompanyForm, CreateContactForm, CreateContactNoCompanyForm, UserForm
from transportation.forms import PickupForm, DeliveryForm


from .help.methods import get_time_flag

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template




def send_confirmation_email(request, contact, products, total_price):
    site_name = get_current_site(request).domain
    max_name_length = max(map(lambda product: len(product[0]), products)) # used for setting width of columns
    max_amount_length = max(map(lambda product: len(str(product[1])), products))
    send_mail(
        'Complete Registration Confirmation on ' + site_name,
        get_template('register/confirmation_email.html').render(({
                'username': contact.email,
                'site_name': site_name,
                'products': products,
                'name_len': max_name_length,
                'amount_len': max_amount_length,
                'total_price': total_price
            })
        ),
        settings.DEFAULT_FROM_EMAIL,
        [contact.email],
        fail_silently=False)



def index(request, template_name='register/index.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is not None:
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:logout')
    timeFlag, [time_end, time_diff] = get_time_flag()
    fair = Fair.objects.filter(current=True).first()
    return render(request, template_name, {'fair': fair, 'timeFlag': timeFlag, 'time_end': time_end, 'time_diff': time_diff})

def preliminary_registration(request,fair, company, contact, contract, exhibitor, signed_up):
    form1 = RegistrationForm(request.POST or None, prefix='registration')
    prev_sale = Sale.objects.filter(fair=fair, company=company).first()
    form2 = InterestForm(request.POST or None, instance=prev_sale,prefix='interest')
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

            form3.save()

            return redirect('anmalan:home')

    return ('register/registration.html', dict(registration_open = True,
                                               signed_up = signed_up,
                                               contact = contact,
                                               company=company,
                                               exhibitor = exhibitor,
                                               fair=fair,
                                               form1=form1,
                                               form2=form2,
                                               form3=form3,
                                               contract_url=contract.contract.url
                                               ))


def get_product_list_and_price(exhibitor):
    orders = Order.objects.filter(exhibitor=exhibitor)
    total_price = sum(map(lambda order: order.product.price * order.amount, orders))
    product_list = list(map(lambda order: [str(order.product.product_type) + ', ' + str(order.product), str(order.amount), str(order.amount*order.product.price)], orders))
    return product_list, total_price



def complete_registration(request,fair, company, contact, contract, exhibitor, signed_up):
    """
    Complete Registration: create_exhibitor view
    ===============
    The complete registration is where already signed up companies with contacts
    can make their final selection of products and send in important info such as
    invoice address ('faktura' in SWE). 

    Extra Info
     ----------------
     * If the user 'saves' then the DB will be updated. If one 'submits' then a
     confirmation email will be sent out.

    """

    included_products = Product.objects.filter(included_for_all=True, fair=fair)
    orders = Order.objects.filter(exhibitor=exhibitor)
    # Create orders of included products if not present
    for product in included_products:
        values_list = orders.values_list('product', flat=True)
        if not product.pk in orders.values_list('product', flat=True):
            Order.objects.create(exhibitor=exhibitor, product=product, amount=1)
    product_list, total_price = get_product_list_and_price(exhibitor)

    forms = [] # this is a list of all forms that is used to collect all errors on start page

    product_type_order_forms = []
    product_types = ProductType.objects.filter(display_in_product_list=True)
    for product_type in product_types:
        order_forms = get_order_forms(exhibitor, product_type, request.POST or None, prefix=product_type.name)
        if not len(order_forms) == 0:
            forms += order_forms
            product_type_order_forms.append((product_type,order_forms))

    electricity_order = ElectricityOrderForm(exhibitor, request.POST or None, 
            instance = ElectricityOrder.objects.filter(exhibitor=exhibitor).first(), prefix='electricity')

    transportation_form = TransportationForm(request.POST or None, instance=exhibitor, prefix='transportation_alternatives')
    forms.append(transportation_form)

    # There should only be a transportation order form if the organization provides transportation services
    inbound_transportation_order_form = None
    if len(TransportationAlternative.objects.filter(inbound=True, transportation_type='internal')) >0:
        inbound_transportation_order_form = PickupForm(request.POST or None, instance=exhibitor.pickup_order,  prefix='inbound_transportation_order')
        forms.append(inbound_transportation_order_form)
    outbound_transportation_order_form = None
    if len(TransportationAlternative.objects.filter(inbound=False, transportation_type='internal')) >0:
        outbound_transportation_order_form = DeliveryForm(request.POST or None, instance=exhibitor.delivery_order,  prefix='outbound_transportation_order')
        forms.append(outbound_transportation_order_form)

    # If post, try and validate and save forms
    if request.POST:
        # Save all the orders of products. (The products that the user has chosen)
        for product_type, order_forms in product_type_order_forms:
            for order_form in order_forms:
                if order_form.is_valid():
                    order_form.save()

        if electricity_order.is_valid():
            electricity_order.save()

        if transportation_form.is_valid():
            transportation_form.save()
        if transportation_form.cleaned_data['inbound_transportation'].transportation_type == 'internal':
            if inbound_transportation_order_form.is_valid():
                inbound_transportation_order_form.save()
        if transportation_form.cleaned_data['outbound_transportation'].transportation_type == 'internal':
            if outbound_transportation_order_form.is_valid():
                outbound_transportation_order_form.save()

        # Check if the user sumbitted or just saved
        if 'submit' in request.POST:
            # Make sure there are no errors at all.
            errors = False
            for form in forms:
                if errors == True:
                    break
                if len(form.non_field_errors()) !=0:
                    errors = True
                    break
                for field in form._errors:
                    if len(form._errors[field])!= 0:
                        errors = True
                        break
            if not errors:
                # Continue with submission, if there were errors, it will just be saved and not submitted, and return to the complete registration
                # Create order log
                orders = Order.objects.filter(exhibitor=exhibitor)
                product_log = "\n".join(map(lambda order: ",".join([str(order.product.product_type), str(order.product), str(order.amount), str(order.amount*order.product.price)]), orders))
                OrderLog.objects.create(contact=contact, company = contact.belongs_to, action='submit', fair=fair, products=product_log)
                # Set progression status
                SignupLog.objects.create(contact=contact, company=company, contract=contract, type='complete')
                exhibitor.status = 'complete_registration_submit'
                exhibitor.save(update_fields=['status'])
                r.post(settings.SALES_HOOK_URL,
                    data=json.dumps({'text': 'User {!s} just submitted complete registration for {!s}!'.format(contact, company)}))

                try:
                    send_email(request, contact, product_list, total_price)
                except:
                    pass
                return redirect('anmalan:submitted')




    return ('register/registration.html', dict(contract_url=contract.contract.url,
                                               complete_registration_open= True,
                                               product_type_order_forms=product_type_order_forms,
                                               electricity_order = electricity_order,
                                               transportation_form = transportation_form,
                                               inbound_transportation_form = inbound_transportation_order_form,
                                               outbound_transportation_form = outbound_transportation_order_form,
                                               forms = forms,
                                               total_price=total_price,
                                               product_list=product_list
                                               )
            )



def home(request, template_name='register/registration.html'):
    if request.user.is_authenticated():
        if Contact.objects.filter(user=request.user).first() is None:
            return redirect('anmalan:logout')
        else:
            forms = [] # this is a list of all forms that is used to collect all errors on start page
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

            contact_form = ContactForm(request.POST or None, instance=contact, prefix='contact_info')
            forms.append(contact_form)
            invoice_details_form = InvoiceDetailsForm(company, request.POST or None, instance=exhibitor.invoice_details, prefix='invoice_details') if exhibitor else None
            forms.append(invoice_details_form)
            company_form = EditCompanyForm(request.POST or None, instance=company, prefix='company_info')
            forms.append(company_form)
            profile_form = ExhibitorProfileForm(request.POST or None, request.FILES or None,  prefix='exhibitor_profile', instance=exhibitor)
            forms.append(profile_form)
            current_matching_survey = Survey.objects.filter(fair=fair).first()
            survey_form = None
            if current_matching_survey:
                survey_form = ResponseForm(current_matching_survey, exhibitor, request.POST or None, prefix='matching')
                forms.append(survey_form)

            if request.POST:
                if company_form.is_valid():
                    company_form.save()
                if contact_form.is_valid():
                    contact_form.save()

                if signed_up and contact.confirmed:
                    # Only check survey form if there is a survey form
                    if survey_form and  survey_form.is_valid():
                        survey_form.save()
                    if profile_form.is_valid():
                        profile_form.save()
                    if invoice_details_form.is_valid():
                        invoice_details_form.save()

            #needs to start check if complete is opened as that should override preliminary
            # There is a risk of having overlapping preliminary and complete registration dates. Therefore we need to check this.
            kwargs = dict(common_forms=forms, company_form=company_form, profile_form=profile_form, 
                        survey_form=survey_form, invoice_details_form=invoice_details_form, contact_form=contact_form, 
                        contact=contact, company=company, exhibitor=exhibitor, fair=fair, signed_up=signed_up)

            if complete_registration_open:
                if signed_up:
                    #return view of complete registration
                    res = complete_registration(request,fair, company, contact, contract, exhibitor, signed_up)
                    if(type(res) == tuple):
                        (template, kwargs_a) = res
                        kwargs.update(kwargs_a)
                        return render(request, template, kwargs)
                    else:
                        return res

            if registration_open:
                res = preliminary_registration(request,fair, company, contact, contract, exhibitor, signed_up)
                if(type(res) == tuple):
                    (template, kwargs_a) = res
                    kwargs.update(kwargs_a)
                    return render(request, template, kwargs)
                else:
                    # here we trust that preliminary registration returns some HTTP response
                    return res

            if registration_closed and not signed_up:
                kwargs.update(dict(registration_closed=registration_closed, signed_up=signed_up))
                return render(request, template_name, kwargs)
                
            if pre_preliminary:
                # this should be basically nothing. Just return with variable, or return a specific template
                kwargs.update(dict(pre_preliminary = pre_preliminary))
                return render(request, template_name, kwargs)

            else:
                #complete_registration_closed is closed
                if signed_up:
                    product_list, total_price = get_product_list_and_price(exhibitor)
                    kwargs.update(dict(complete_registration_closed=complete_registration_closed, signed_up=signed_up,
                                        product_list=product_list, total_price=total_price))
                    return render(request, template_name, kwargs)
                else:
                    kwargs.update(dict(complete_registration_closed=complete_registration_closed, signed_up=signed_up))
                    return render(request, template_name, kwargs)

    return redirect('anmalan:index')


def create_new_exhibitor_from_old(old_exhibitor, contact, fair):
    exhibitor = Exhibitor.objects.create(fair=fair, status='registered',
            company=old_exhibitor.company,
            contact=contact,
            about_text = old_exhibitor.about_text,
            logo = old_exhibitor.logo,
            invoice_details = old_exhibitor.invoice_detials,
            )
    # ManyToMany fields needs to be copied after creation
    # the * unpacks the list, taking [a,b,c] to a,b,c
    exhibitor.job_types.add(*old_exhibitor.job_types.all())
    exhibitor.save()
    return exhibitor

def signup(request, template_name='register/create_user.html'):
    contact_form = CreateContactForm(request.POST or None, prefix='contact')
    user_form = UserForm(request.POST or None, prefix='user')
    if request.POST and contact_form.is_valid() and user_form.is_valid():
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


# thank you screen after submission of complete registration
def submission_view(request, template_name='register/finished_registration.html'):
    fair = Fair.objects.filter(current=True).first()
    return render(request, template_name, dict(fair=fair))


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
