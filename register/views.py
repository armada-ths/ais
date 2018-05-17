from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings

import requests as r
import json

from companies.models import Company, CompanyCustomer, CompanyContact
from orders.models import Product, Order, ProductType, ElectricityOrder
from exhibitors.models import Exhibitor, TransportationAlternative
from fair.models import Fair
from matching.models import Survey

from .models import SignupContract, SignupLog

from .forms import RegistrationForm, ChangePasswordForm
from orders.forms import SelectStandAreaForm, get_order_forms, ElectricityOrderForm
from exhibitors.forms import ExhibitorProfileForm, TransportationForm
from matching.forms import ResponseForm
from companies.forms import CompanyForm, CompanyContactForm, CreateCompanyContactForm, CreateCompanyContactNoCompanyForm, UserForm
from transportation.forms import PickupForm, DeliveryForm


from .help.methods import get_time_flag

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template


def index(request, template_name='register/index.html'):
    if request.user.is_authenticated():
        if CompanyContact.objects.filter(user=request.user).first() is not None:
            return redirect('anmalan:home')
        else:
            return redirect('anmalan:logout')
    timeFlag, [time_end, time_diff] = get_time_flag()
    fair = Fair.objects.filter(current=True).first()
    return render(request, template_name, {'fair': fair, 'timeFlag': timeFlag, 'time_end': time_end, 'time_diff': time_diff})

def signup(request, template_name='register/create_user.html'):
	contact_form = CreateCompanyContactForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')

	if request.POST and contact_form.is_valid() and user_form.is_valid():
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:home')
	
	return render(request, template_name, dict(contact_form=contact_form, user_form=user_form))

def create_company(request, template_name='register/company_form.html'):
	form = CompanyForm(request.POST or None)
	contact_form = CreateCompanyContactNoCompanyForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')

	if contact_form.is_valid() and user_form.is_valid() and form.is_valid(None):
		company = form.save()
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.confirmed = True #Auto confirm contacts who register a new company
		contact.company = company
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:home')
	return render(request, template_name, dict(form=form, contact_form=contact_form, user_form=user_form))


def submission_view(request, template_name='register/finished_registration.html'):
    """
    Thank you screen after submission of complete registration
    """
    fair = Fair.objects.filter(current=True).first()
    contact = CompanyContact.objects.get(user=request.user)
    company = contact.company
    exhibitor = Exhibitor.objects.filter(company=company, fair=fair).first()
    product_list, total_price = get_product_list_and_price(exhibitor);
    return render(request, template_name, dict(fair=fair, product_list=product_list, total_price=total_price))


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


def create_new_exhibitor_from_old(old_exhibitor, contact, fair):
    """
    Helper function for preliminary registration to copy information from last year for an exhibitor
    """
    exhibitor = Exhibitor.objects.create(fair=fair, status='registered',
            company=old_exhibitor.company,
            contact=contact,
            about_text = old_exhibitor.about_text,
            logo = old_exhibitor.logo,
            )
    # ManyToMany fields needs to be copied after creation
    # the * unpacks the list, taking [a,b,c] to a,b,c
    exhibitor.job_types.add(*old_exhibitor.job_types.all())
    exhibitor.save()
    return exhibitor

def preliminary_registration(request, fair, company, contact, contract, exhibitor, signed_up, allow_saving, company_customer):
	form = RegistrationForm((request.POST or None) if allow_saving else None, prefix = 'registration', instance = company_customer)

	if not signed_up and form.is_valid():
		print("form.cleaned_data[\"groups\"] = " + str(form.cleaned_data["groups"]))
		print("company_customer.groups.all() = " + str(company_customer.groups.all()))
		form.cleaned_data["groups"] = company_customer.groups.union(form.cleaned_data["groups"])
		print("form.cleaned_data[\"groups\"] = " + str(form.cleaned_data["groups"]))
		form.save()
		SignupLog.objects.create(company_contact = contact, contract = contract, company = contact.company)

		return redirect('anmalan:home')

	return ('register/registration.html', dict(registration_open = True, signed_up = signed_up, contact = contact, company=company, exhibitor = exhibitor, fair=fair, form = form, contract_url = contract.contract.url if contract else None ))


def get_product_list_and_price(exhibitor):
    """ 
    Get a list of all products that the exhibitor has ordered and the total price of them.
    returns a tuple: product_list, total_price
    """
    orders = Order.objects.filter(exhibitor=exhibitor)
    total_price = sum(map(lambda order: order.product.price * order.amount, orders))
    product_list = list(map(lambda order: [str(order.product.product_type) + ', ' + str(order.product), str(order.amount), str(order.amount*order.product.price)], orders))
    return product_list, total_price

def create_orders_for_included_products(fair, exhibitor):
    """ 
    Some products are marked as included for everyone. 
    If these products are not added to exhibitor, they will be added
    """
    included_products = Product.objects.filter(included_for_all=True, fair=fair)
    orders = Order.objects.filter(exhibitor=exhibitor)
    # Create orders of included products if not present
    for product in included_products:
        values_list = orders.values_list('product', flat=True)
        if not product.pk in orders.values_list('product', flat=True):
            Order.objects.create(exhibitor=exhibitor, product=product, amount=1)

def get_product_type_order_forms(request, exhibitor, forms):
    """ 
    Get a list of order forms, grouped by their product category
    """
    product_type_order_forms = []
    product_types = ProductType.objects.filter(display_in_product_list=True)
    for product_type in product_types:
        order_forms = get_order_forms(exhibitor, product_type, request.POST or None, prefix=product_type.name)
        if not len(order_forms) == 0:
            forms += order_forms
            product_type_order_forms.append((product_type,order_forms))
    return product_type_order_forms


def save_complete_registration(product_type_ordor_forms, electricity_order, transportation_form, 
        inbound_transportation_order_form, outbound_transportation_order_form):
    """ Validate and try to save all the provided forms """

    # Save all the orders of products. (The products that the user has chosen)
    for product_type, order_forms in product_type_order_forms:
        for order_form in order_forms:
            if order_form.is_valid():
                order_form.save()
    
    if electricity_order.is_valid():
        electricity_order.save()

    if transportation_form.is_valid():
        transportation_form.save()
    inbound_transport = transportation_form.cleaned_data['inbound_transportation']
    if inbound_transport and inbound_transport.transportation_type == 'internal':
        if inbound_transportation_order_form.is_valid():
            inbound_transportation_order_form.save()
    outbound_transport = transportation_form.cleaned_data['outbound_transportation']
    if outbound_transport and outbound_transport.transportation_type == 'internal':
        if outbound_transportation_order_form.is_valid():
            outbound_transportation_order_form.save()

def check_form_errors(forms):
    """
    Iterate through every form in forms and check if any has errors
    returns True if there are errors, otherwise False
    """
    for form in forms:
        if len(form.non_field_errors()) !=0:
            return True
        for field in form._errors:
            if len(form._errors[field])!= 0:
                return True
    return False

def create_sumbission(exhibitor, contact, fair, contract):
	"""
	Create objects in database for a sumbission of the complete registration
	"""
	# Create order log
	orders = Order.objects.filter(exhibitor=exhibitor)
	product_log = "\n".join(map(lambda order: ",".join([str(order.product.product_type), str(order.product), str(order.amount), str(order.amount*order.product.price)]), orders))

	# Set progression status
	SignupLog.objects.create(company_contact = contact, company = contact.company, contract = contract, type = 'complete')

	exhibitor.status = 'complete_registration_submit'
	exhibitor.accept_terms = True
	exhibitor.save(update_fields=['status', 'accept_terms'])

	r.post(settings.SALES_HOOK_URL,
		data=json.dumps({'text': 'User {!s} just submitted complete registration for {!s}!'.format(contact, contact.company)}))

def send_confirmation_email(request, contact, products, total_price):
    try:
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
    except:
        pass



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

    ######## Create orders and build the product list #########
    create_orders_for_included_products(fair, exhibitor)
    product_list, total_price = get_product_list_and_price(exhibitor)

    ######### Create required forms ##########
    forms = [] # this is a list of all forms that is used to collect all errors on start page
    product_type_order_forms = get_product_type_order_forms(request, exhibitor, forms)
    electricity_order = ElectricityOrderForm(exhibitor, request.POST or None, 
            instance = ElectricityOrder.objects.filter(exhibitor=exhibitor).first(), prefix='electricity')
    forms.append(electricity_order)
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


    ###### Try to validate and save forms if it is a post request ########
    if request.POST:
        save_complete_registration(product_type_order_forms, electricity_order, transportation_form,
                inbound_transportation_order_form, outbound_transportation_order_form)
        #Update the product list and price after saving
        product_list, total_price = get_product_list_and_price(exhibitor)

        # Check if the user sumbitted or just saved
        if 'submit' in request.POST:
            errors = check_form_errors(forms)
            if not errors:
                # Continue with submission, if there were errors, it will just be saved and not submitted, and return to the complete registration
                create_sumbission(exhibitor, contact, fair, contract)

                # Try to send out a confirmation email
                send_confirmation_email(request, contact, product_list, total_price)

                # Return by redirecting to the page that says the regirstation is completed and sumbitted
                return redirect('anmalan:submitted')

    # Default behaviour on a get request. Show the complete registration
    return ('register/registration.html', dict(contract_url=contract.contract.url if contract else None,
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
	"""
	If there is no logged in company user that is associated with a contact object, 
	they will be logged out and redirected to the index page.

	This view controls what stage the registration is in. 
	There are five different stages:
	1. Before any registration is open, this is just when a new fair has been created and the registration period has not started yet.
	2. The preliminary registration period has started. 
	3. The preliminary registration period has ended and the complete registration has not opened yet. Note that it is possible to have overlapping
	preliminary and complete registration periods. Then this stage would not exist.
	4. The  complete registration has opened.
	5. The complete registration has closed.

	Depending on what stage is present, this view routes to different other views and builds up the data object to send to the templates.

	This view also creates forms and variables that are common for all stages.
	"""
	if request.user.is_authenticated():
		if CompanyContact.objects.filter(user = request.user).first() is None:
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
			
			contact = CompanyContact.objects.get(user=request.user)
			company = contact.company
			
			company_customer = CompanyCustomer.objects.filter(fair = fair, company = contact.company).first()
			
			if company_customer is None:
				company_customer = CompanyCustomer.objects.create(company = contact.company, fair = fair)
			
			contract = SignupContract.objects.filter(fair=fair, current=True).first()
			
			for group in company_customer.groups.all():
				if group.contract is not None:
					contract = group.contract
					break
			
			exhibitor = Exhibitor.objects.filter(company=company, fair=fair).first()
			signed_up = SignupLog.objects.filter(company = company, contract = contract).first() != None

			contact_form = CompanyContactForm(request.POST or None, instance = contact, prefix = 'contact_info')
			del contact_form.fields["active"]
			del contact_form.fields["confirmed"]
			forms.append(contact_form)
			
			#invoice_details_form = InvoiceDetailsForm(company, request.POST or None, instance=exhibitor.invoice_details, prefix='invoice_details') if exhibitor else None
			#forms.append(invoice_details_form)
			
			company_form = CompanyForm(request.POST or None, instance = company, prefix = 'company_info')
			forms.append(company_form)
			
			#profile_form = ExhibitorProfileForm(request.POST or None, request.FILES or None,  prefix='exhibitor_profile', instance=exhibitor)
			#forms.append(profile_form)
			
			current_matching_survey = Survey.objects.filter(fair=fair).first()
			survey_form = None
			
			if current_matching_survey:
				survey_form = ResponseForm(current_matching_survey, exhibitor, request.POST or None, prefix='matching')
				forms.append(survey_form)

			if request.POST:
				if company_form.is_valid(company):
					company_form.save()
				
				if contact_form.is_valid():
					contact_form.save()

				if signed_up and contact.confirmed:
				# Only check survey form if there is a survey form
					if survey_form and  survey_form.is_valid():
						survey_form.save()

			#needs to start check if complete is opened as that should override preliminary
			# There is a risk of having overlapping preliminary and complete registration dates. Therefore we need to check this.
			kwargs = dict(common_forms=forms, company_form=company_form, profile_form=None, survey_form=survey_form, contact_form=contact_form,  contact=contact, company=company, exhibitor=exhibitor, fair=fair, signed_up=signed_up)

			if complete_registration_open:
				if signed_up:
					#return view of complete registration
					res = complete_registration(request,fair, company, contact, contract, exhibitor, signed_up)
				
				if type(res) == tuple:
					(template, kwargs_a) = res
					kwargs.update(kwargs_a)
					return render(request, template, kwargs)
				else:
					return res

			if registration_open:
				res = preliminary_registration(request,fair, company, contact, contract, exhibitor, signed_up, 'save' not in request.POST, company_customer)
				
				if type(res) == tuple:
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
					kwargs.update(dict(complete_registration_closed=complete_registration_closed, signed_up=signed_up, product_list=product_list, total_price=total_price))
					return render(request, template_name, kwargs)
				
				else:
					kwargs.update(dict(complete_registration_closed=complete_registration_closed, signed_up=signed_up))
					return render(request, template_name, kwargs)

	return redirect('anmalan:index')
