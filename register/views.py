from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site

from collections import namedtuple
import math

import json
import requests as r

from companies.models import Company, Contact
from orders.models import Product, Order, ProductType
from exhibitors.models import Exhibitor
from fair.models import Fair
from sales.models import Sale
from matching.models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns
from .models import SignupContract, SignupLog

from .forms import CompanyForm, ContactForm, RegistrationForm, CreateContactForm, UserForm, InterestForm, ExhibitorForm, ChangePasswordForm

BASE_PRICE = 39500




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
    currentFair = Fair.objects.get(current = True)
    contract = SignupContract.objects.get(fair=currentFair, current=True)
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
                exhibitor = Exhibitor.objects.get(company=company)
            except Exhibitor.DoesNotExist:
                pass

            # Get products which requires an amount and put them into the Exhibitor form
            banquet_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Banquet"))
            lunch_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="AdditionalLunch"))
            event_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Events"))
            room_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Rooms"))
            nova_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Nova"))
            stand_area_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Additional Stand Area"))
            stand_height_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Additional Stand Height"))

            # Check which products that already is in an order
            current_banquet_orders = Order.objects.filter(exhibitor=exhibitor, product__in=banquet_products)
            current_lunch_orders = Order.objects.filter(exhibitor=exhibitor, product__in=lunch_products)
            current_event_orders = Order.objects.filter(exhibitor=exhibitor, product__in=event_products)
            current_room_orders = Order.objects.filter(exhibitor=exhibitor, product__in=room_products)
            current_nova_orders = Order.objects.filter(exhibitor=exhibitor, product__in=nova_products)
            current_stand_area_orders = Order.objects.filter(exhibitor=exhibitor, product__in=stand_area_products)
            current_stand_height_orders = Order.objects.filter(exhibitor=exhibitor, product__in=stand_height_products)

            # get survey and corresponding matching questions
            matching_survey = Survey.objects.get(fair=currentFair, name='exhibitor-matching')
            matching_questions = Question.objects.filter(survey=matching_survey)
            # check which questions are already answered
            current_matching_responses = Response.objects.filter(exhibitor=exhibitor, survey=matching_survey)
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
            )

            if form.is_valid():
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
                exhibitor.fair = currentFair

                # Create or update exhibitor
                try:
                    exhibitor.pk = Exhibitor.objects.get(company=exhibitor.company).pk
                    exhibitor.save()
                except Exhibitor.DoesNotExist:
                    exhibitor.save()

                # create or update orders to the current exhibitor from products
                def create_or_update_order(product, amount):
                        order = None
                        try:
                            order = Order.objects.get(product=product,exhibitor=exhibitor)
                            order.amount = amount
                            order.save()
                        except Order.DoesNotExist:
                            order = Order.objects.create(
                                exhibitor=exhibitor,
                                product=product,
                                amount=amount,
                            )
                # delete an order via a product and the current exhibitor
                def delete_order_if_exists(product):
                    try:
                        Order.objects.get(product=product, exhibitor=exhibitor).delete()
                    except Order.DoesNotExist:
                        return

                # Create or update orders from the checkbox products (ProductMultiChoiceField).
                # If they are not checked in but exist as an order in db, then delete.
                room_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Rooms"))
                nova_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Nova"))
                stand_area_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Area"))
                stand_height_products = Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Height"))

                # Boolean (checkmark) products
                bool_products = []
				# TODO fetch prices from elsewhere
                total_price = BASE_PRICE


                for product in room_products:
                    if product in product_selection_rooms:
                        bool_products.append(product)
                        total_price += product.price
                        create_or_update_order(product, 1)
                    else:
                        delete_order_if_exists(product)
                for product in nova_products:
                    if product in product_selection_nova:
                        bool_products.append(product)
                        total_price += product.price
                        create_or_update_order(product, 1)
                    else:
                        delete_order_if_exists(product)
                for product in stand_area_products:
                    if product.name in product_selection_additional_stand_area:
                        bool_products.append(product)
                        total_price += product.price
                        create_or_update_order(product, 1)
                    else:
                        delete_order_if_exists(product)
                for product in stand_height_products:
                    if product.name in product_selection_additional_stand_height:
                        bool_products.append(product)
                        total_price += product.price
                        create_or_update_order(product, 1)
                    else:
                        delete_order_if_exists(product)

				# Numerical (amount) products
                num_products = []
                NumProduct = namedtuple('NumProduct', ['name', 'amount', 'price'])

                # Create or update orders from products that can be chosen in numbers.
                # If they have an amount equal to zero then delete the order.
                for (banquetProduct, amount) in form.amount_products('banquet_'):
                    if amount > 0:
                        create_or_update_order(banquetProduct, amount)
                        num_products.append(NumProduct(banquetProduct.name, amount, amount * banquetProduct.price))
                        total_price += amount * banquetProduct.price
                    else:
                        delete_order_if_exists(banquetProduct)

                for (lunchProduct, amount) in form.amount_products('lunch_'):
                    if amount > 0:
                        create_or_update_order(lunchProduct, amount)
                        num_products.append(NumProduct(lunchProduct.name, amount, amount * lunchProduct.price))
                        total_price += amount * lunchProduct.price
                    else:
                        delete_order_if_exists(lunchProduct)

                for (eventProduct, amount) in form.amount_products('event_'):
                    if amount > 0:
                        create_or_update_order(eventProduct, amount)
                        num_products.append(NumProduct(eventProduct.name, amount, amount * eventProduct.price))
                        total_price += amount * eventProduct.price
                    else:
                        delete_order_if_exists(eventProduct)

				# Longest name length for padding purposes
                def getNameLen(item):
                    return len(item.name)
                def getAmount(item):
                    return item.amount
                

                if bool_products:
                    max_name_len_bool = len(max(bool_products, key=getNameLen).name)
                else:
                    max_name_len_bool = 0

                if num_products:
                    max_name_len_num = len(max(num_products, key=getNameLen).name)
                    max_amount = math.ceil(max(num_products, key=getAmount).amount / 10)
                else:
                    max_name_len_num = 0
                    max_amount = 0
                
                max_name_len = max(max_name_len_bool, max_name_len_num)



                # Add the Base Kit (mandatory) and Banquet ticket - Base Kit (2 are included)
                # If already added, don't add to db, else add.
                base_kit_products = Product.objects.filter(fair=currentFair, product_type=ProductType.objects.filter(name="Base Kit"))
                current_base_kit_orders = Order.objects.filter(exhibitor=exhibitor, product__in=base_kit_products)

                for product in base_kit_products:
                    if product.name == "Banquet Ticket - Base Kit":  # 2 Banquet tickets are included
                        amount = 2
                    else:
                        amount = 1

                    if not product in current_base_kit_orders:
                        create_or_update_order(product, amount)

                def create_or_update_answer(response, question, ans):
                    answer = None
                    if question.question_type == Question.TEXT:
                        try:
                            answer = TextAns.objects.get(question=question, response=response)
                            answer.ans = ans
                            answer.save()
                        except TextAns.DoesNotExist:
                            answer = TextAns.objects.create(question=question, response = response, ans=ans)
                    elif question.question_type == Question.INT:
                        try:
                            answer = IntegerAns.objects.get(question=question, response=response)
                            answer.ans = ans
                            answer.save()
                        except IntegerAns.DoesNotExist:
                            answer = IntegerAns.objects.create(question=question, response = response, ans=ans)
                    elif question.question_type == Question.SELECT:
                        try:
                            answer = ChoiceAns.objects.get(question=question, response=response)
                            answer.ans = ans
                            answer.save()
                        except ChoiceAns.DoesNotExist:
                            answer = ChoiceAns.objects.create(question=question, response = response, ans=ans)
                    elif question.question_type == Question.BOOL:
                        try:
                            answer = BooleanAns.objects.get(question=question, response=response)
                            answer.ans = ans
                            answer.save()
                        except BooleanAns.DoesNotExist:
                            answer = BooleanAns.objects.create(question=question, response = response, ans=ans)


                # create or update responses on matching questions
                def create_or_update_response(question, ans):
                    response = None
                    try:
                        response = Response.objects.get(exhibitor=exhibitor, question=question, survey=matching_survey)
                        #response.save()
                    except Response.DoesNotExist:
                        response = Response.objects.create(exhibitor=exhibitor, survey=matching_survey, question=question)
                    create_or_update_answer(response, question, ans)


                #delete response via question and current exhibitor
                def delete_response_if_exists(question, ans):
                    try:
                        Response.objects.get(exhibitor=exhibitor, survey=matching_survey, question=question).delete()
                    except Response.DoesNotExist:
                        return

                # get answers from form
                prefix='question_' #note this is hard coded in forms as well
                for q in matching_questions:
                    ans = form.cleaned_data['%s%d'%(prefix,q.pk)]
                    if ans:
                        create_or_update_response(q, ans)
                    else:
                        delete_response_if_exists(q, ans)


                # Contract agreement
                def create_signup():
                    signup = None
                    try:
                        signup = SignupLog.objects.get(contact=contact, contract=contract, company = contact.belongs_to)
                    except SignupLog.DoesNotExist:
                        signup = SignupLog.objects.create(contact=contact, contract=contract, company = contact.belongs_to, type = 'complete')

                if form.accepting_terms():
                    create_signup()


                # Everything is done!
                # Do nothing if form is saved, otherwise redirect and send email
                save_or_submit = form.save_or_submit()
                if 'submit' in save_or_submit:
                    r.post(settings.SALES_HOOK_URL,
                        data=json.dumps({'text': 'User {!s} just submitted complete registration for {!s}!'.format(contact, company)}))

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
                    return redirect('anmalan:cr_done')

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
