from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template

from collections import namedtuple

import math
import json
import requests as r

from fair.models import Fair
from exhibitors.models import Exhibitor
from companies.models import Company, Contact
from register.forms import ExhibitorForm
from register.models import SignupContract, OrderLog
from orders.models import Product, Order, ProductType
from matching.models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns

from .methods import get_time_flag, create_signup, create_or_update_order, delete_order_if_exists, \
create_or_update_answer, create_or_update_response, delete_response_if_exists, product_amount_string


BASE_PRICE = 39500
BASE_PRODUCT_NAME = 'Base Kit \n'
PRODUCT_LOG = ":"

NumProduct = namedtuple('NumProduct', ['name', 'amount', 'price'])


def create_exhibitor_form(request, fair, exhibitor, company, contact):
    # Get products which requires an amount and put them into the Exhibitor form
    banquet_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Banquet"))
    lunch_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="AdditionalLunch"))
    event_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Events"))
    room_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Rooms"))
    nova_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Nova"))
    stand_area_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Additional Stand Area"))
    stand_height_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Additional Stand Height"))

    # Check which products that already is in an order
    current_banquet_orders = Order.objects.filter(exhibitor=exhibitor, product__in=banquet_products)
    current_lunch_orders = Order.objects.filter(exhibitor=exhibitor, product__in=lunch_products)
    current_event_orders = Order.objects.filter(exhibitor=exhibitor, product__in=event_products)
    current_room_orders = Order.objects.filter(exhibitor=exhibitor, product__in=room_products)
    current_nova_orders = Order.objects.filter(exhibitor=exhibitor, product__in=nova_products)
    current_stand_area_orders = Order.objects.filter(exhibitor=exhibitor, product__in=stand_area_products)
    current_stand_height_orders = Order.objects.filter(exhibitor=exhibitor, product__in=stand_height_products)

    # get survey and corresponding matching questions
    try:
        matching_survey = Survey.objects.get(fair=fair, name='exhibitor-matching')
    except Survey.DoesNotExist:
        matching_survey = None
    matching_questions = Question.objects.filter(survey=matching_survey)
    # check which questions are already answered
    current_matching_responses = Response.objects.filter(exhibitor=exhibitor, survey=matching_survey)

    # Set automated time closing of cr
    timeFlag, time_disp = get_time_flag()

    # Pass along all relevant information to form
    form = ExhibitorForm(
        request.POST or None,
        request.FILES or None,
        instance = exhibitor,
        banquet = banquet_products,
        lunch = lunch_products,
        events = event_products,
        rooms = room_products,
        nova = nova_products,
        stand_area = stand_area_products,
        stand_height = stand_height_products,
        banquet_orders = current_banquet_orders,
        lunch_orders = current_lunch_orders,
        event_orders = current_event_orders,
        room_orders = current_room_orders,
        nova_orders = current_nova_orders,
        stand_area_orders = current_stand_area_orders,
        stand_height_orders = current_stand_height_orders,
        company = company,
        contact = contact,
        matching_survey = matching_survey,
        matching_questions = matching_questions,
        matching_responses = current_matching_responses,
        timeFlag = timeFlag,
        time_disp = time_disp,
    )

    return form


def save_exhibitor_form(request, form, fair, company, contact):

    # get selected products. IMPORTANT: NEEDS TO BE BEFORE form.save(commit=False)
    product_selection_rooms = form.cleaned_data['product_selection_rooms']
    product_selection_nova = form.cleaned_data['product_selection_nova']
    product_selection_additional_stand_area = form.cleaned_data['product_selection_additional_stand_area']
    product_selection_additional_stand_height = form.cleaned_data['product_selection_additional_stand_height']

    # Save exhibitor model values from form into exhibitor variable
    exhibitor = form.save(commit=False)

    # Update Company fields
    updatedCompany = Company.objects.get(pk=company.pk)
    updatedCompany.organisation_number = form.cleaned_data['organisation_identification_number']
    updatedCompany.organisation_type = form.cleaned_data['type_of_organisation']
    updatedCompany.address_street = form.cleaned_data['address_street']
    updatedCompany.address_zip_code = form.cleaned_data['address_zip_code']
    updatedCompany.address_city = form.cleaned_data['address_city']
    updatedCompany.address_country = form.cleaned_data['address_country']
    updatedCompany.additional_address_information = form.cleaned_data['additional_address_information']
    updatedCompany.website = form.cleaned_data['website']
    updatedCompany.save()
    exhibitor.company = updatedCompany

    # Update Contact fields
    updatedContact = Contact.objects.get(pk=contact.pk)
    updatedContact.name = form.cleaned_data['contact_name']
    updatedContact.work_phone = form.cleaned_data['work_phone']
    updatedContact.cell_phone = form.cleaned_data['cell_phone']
    updatedContact.phone_switchboard = form.cleaned_data['phone_switchboard']
    updatedContact.email = form.cleaned_data['contact_email']
    updatedContact.alternative_email = form.cleaned_data['alternative_email']
    updatedContact.save()
    exhibitor.contact = updatedContact

    # other exhibitor fields that you do not choose in the form
    exhibitor.fair = fair

    # Create or update exhibitor
    try:
        exhibitor.pk = Exhibitor.objects.get(company=exhibitor.company, fair=fair).pk
        exhibitor.save()
    except Exhibitor.DoesNotExist:
        exhibitor.save()

    # Create or update orders from the checkbox products (ProductMultiChoiceField).
    # If they are not checked in but exist as an order in db, then delete.
    room_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Rooms"))
    nova_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Nova"))
    stand_area_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Area"))
    stand_height_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Height"))

    # Boolean (checkmark) products
    bool_products = []
	# TODO fetch prices from elsewhere
    total_price = BASE_PRICE    # total_price and product_log are updated within process_x functions
    product_log = BASE_PRODUCT_NAME

    # process boolean orders
    for product in room_products:
        (total_price, product_log) = process_product(product, product_selection_rooms, exhibitor, bool_products, total_price, product_log)
    for product in nova_products:
        (total_price, product_log) = process_product(product, product_selection_nova, exhibitor, bool_products, total_price, product_log)

    # process option orders
    for product in stand_area_products:
        (total_price, product_log) = process_option_product(product, product_selection_additional_stand_area, exhibitor, bool_products, total_price, product_log)
    for product in stand_height_products:
        (total_price, product_log) = process_option_product(product, product_selection_additional_stand_height, exhibitor, bool_products, total_price, product_log)

	# Numerical (amount) products
    num_products = []
    
    # process numerical orders
    (total_price, product_log) = process_num_orders(form, 'banquet_', exhibitor, num_products, total_price, product_log)
    (total_price, product_log) = process_num_orders(form, 'lunch_', exhibitor, num_products, total_price, product_log)
    (total_price, product_log) = process_num_orders(form, 'event_', exhibitor, num_products, total_price, product_log)

	# Longest name length for padding purposes
    def getNameLen(item):
        return len(item.name)
    def getAmount(item):
        return item.amount

    max_name_len_bool = 0
    max_name_len_num = 0
    max_amount = 0

    if bool_products:
        max_name_len_bool = len(max(bool_products, key=getNameLen).name)

    if num_products:
        max_name_len_num = len(max(num_products, key=getNameLen).name)
        max_amount = math.ceil(max(num_products, key=getAmount).amount / 10)

    max_name_len = max(max_name_len_bool, max_name_len_num)


    # Add the Base Kit (mandatory) and Banquet ticket - Base Kit (2 are included)
    # If already added, don't add to db, else add.
    base_kit_products = Product.objects.filter(fair=fair, product_type=ProductType.objects.filter(name="Base Kit"))
    current_base_kit_orders = Order.objects.filter(exhibitor=exhibitor, product__in=base_kit_products)

    for product in base_kit_products:
        if product.name == "Banquet Ticket - Base Kit":  # 2 Banquet tickets are included
            amount = 2
        else:
            amount = 1

        if not product in current_base_kit_orders:
            create_or_update_order(product, amount, exhibitor)

    try:
        matching_survey = Survey.objects.get(fair=fair, name='exhibitor-matching')
    except Survey.DoesNotExist:
        matching_survey = None
    matching_questions = Question.objects.filter(survey=matching_survey)
    # get answers from form
    prefix='question_' #note this is hard coded in forms as well
    for q in matching_questions:
        ans = form.cleaned_data['%s%d'%(prefix,q.pk)]
        if ans:
            create_or_update_response(q, ans, exhibitor)
        else:
            delete_response_if_exists(q, ans, exhibitor)


    # set exhibitor status to in progres if not already submitted
    if exhibitor.status != 'complete_registration_submit' and exhibitor.status != 'complete_registration':
        exhibitor.status = 'complete_registration_start'
        exhibitor.save()

    if form.accepting_terms():
        create_signup(contact, SignupContract.objects.get(fair=fair, current=True))

    # Everything is done!
    # Do nothing if form is saved, otherwise redirect and send email
    save_or_submit = form.save_or_submit()
    if 'submit' in save_or_submit:
        r.post(settings.SALES_HOOK_URL,
            data=json.dumps({'text': 'User {!s} just submitted complete registration for {!s}!'.format(contact, company)}))

        # log
        log = OrderLog.objects.create(contact=contact, company = contact.belongs_to, action='submit', fair=Fair.objects.get(current=True), products=product_log)
        log.save()

        # send email
        site_name = get_current_site(request).domain
        send_mail(
            'Complete Registration Confirmation on ' + site_name,
            get_template('register/complete_confirm_email.html').render(({
                    'username': contact.email,
                    'site_name': site_name,
                    'bool_products': bool_products,
					'num_products': num_products,
                    'amount_len':max_amount,
                    'name_len': max_name_len,
					'base_price': BASE_PRICE,
                    'total_price': total_price
                })
            ),
            settings.DEFAULT_FROM_EMAIL,
            [contact.email],
            fail_silently=False)

        # set exhibitor status to CR - submitted
        if exhibitor.status != 'complete_registration':
            exhibitor.status = 'complete_registration_submit'
            exhibitor.save()

        return redirect('anmalan:cr_done')
    else:
        # create OrderLog
        log = OrderLog.objects.create(contact=contact, company = contact.belongs_to, action='save', fair=Fair.objects.get(current=True), products=product_log)
        log.save()
#end of save_exhibitor_form()


def process_product(product, selection, exhibitor, bool_products, total_price, product_log):
    if product in selection:
        bool_products.append(product)
        total_price += product.price
        create_or_update_order(product, 1, exhibitor)
        product_log += product_amount_string(product, 1)
    else:
        delete_order_if_exists(product, exhibitor)
    return (total_price, product_log)


def process_option_product(product, selection, exhibitor, bool_products, total_price, product_log):
    # this is a fix due to replace in products_as_select_field foo in register/forms.py, which is needed for the js that generates a product list in the confirm and submit tab
    option = str(product.name)
    option = option.replace(" ", "")
    option = option.replace(",", "_")
    if option in selection:
        bool_products.append(product)
        total_price += product.price
        create_or_update_order(product, 1, exhibitor)
        product_log += product_amount_string(product, 1)
    else:
        delete_order_if_exists(product, exhibitor)
    return (total_price, product_log)


# Create or update orders from products that can be chosen in numbers.
# If they have an amount equal to zero then delete the order.
# Try if amount is None
def process_num_orders(form, prefix, exhibitor, num_products, total_price, product_log):
    for (product, amount) in form.amount_products(prefix):
        try:
            if amount > 0:
                create_or_update_order(product, amount, exhibitor)
                product_log += product_amount_string(product, amount)
                num_products.append(NumProduct(product.name, amount, amount * product.price))
                total_price += amount * product.price
            else:
                delete_order_if_exists(product, exhibitor)
        except TypeError:
            amount = 0
            delete_order_if_exists(product, exhibitor)
    return (total_price, product_log)
