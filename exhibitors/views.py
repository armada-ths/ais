from django.forms import modelform_factory, TextInput
from django.http import HttpResponseForbidden
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import get_connection, EmailMultiAlternatives, send_mail
from django.contrib.auth.decorators import permission_required


from companies.models import Company, CompanyContact
from django.urls import reverse
from fair.models import Fair
from accounting.models import Product, Order
from register.models import SignupLog

from .forms import ExhibitorViewForm, ExhibitorFormFull, ExhibitorFormPartial, ExhibitorCreateForm, TransportForm
from .models import Exhibitor, ExhibitorView

import logging

def user_can_modify_exhibitor(user, exhibitor):
    return user.has_perm(
        'exhibitors.change_exhibitor') or user in exhibitor.hosts.all() or user in exhibitor.superiors()

@permission_required('exhibitors.base')
def exhibitors(request, year, template_name='exhibitors/exhibitors.html'):
    if not request.user.has_perm('exhibitors.base'):
        return HttpResponseForbidden()
    fair = get_object_or_404(Fair, year=year)


    view = ExhibitorView.objects.filter(user=request.user).first()
    if not view: view = ExhibitorView(user=request.user).create()
    fields = view.choices.split(' ')
    fields.remove('')

    return render(request, template_name, {
        'exhibitors': Exhibitor.objects.prefetch_related('hosts').filter(fair=fair).order_by('company__name'),
        'fields' : fields,
        'fair': fair
    })


@permission_required('exhibitors.base')
def edit_view(request, year, template_name='exhibitors/edit_view.html'):
    view = ExhibitorView.objects.filter(user=request.user).first()
    form = ExhibitorViewForm(request.POST or None, instance=view, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('exhibitors', year)

    return render(request, template_name, {
        'form': form,
        'fair': get_object_or_404(Fair, year=year, current=True)
    })


@permission_required('exhibitors.base')
def create(request, year):
	fair = get_object_or_404(Fair, year = year, current = True)
	exhibitors = Exhibitor.objects.filter(fair = fair)
	companies_already_added = []
	
	for exhibitor in exhibitors:
		companies_already_added.append(exhibitor.company)
	
	signatures = SignupLog.objects.filter(contract__fair = fair)
	companies = []
	
	for signature in signatures:
		if signature.company not in companies and signature.company not in companies_already_added:
			companies.append(signature.company)
	
	if len(companies) != 0:
		form = ExhibitorCreateForm(request.POST or None)
		
		companies.sort(key = lambda x: x.name)
		form.fields['companies'].choices = [(company.pk, company.name) for company in companies]
		
		if request.POST and form.is_valid():
			for company in form.cleaned_data['companies']:
				if company in companies:
					exhibitor = Exhibitor.objects.create(fair = fair, company = company)
					exhibitor.save()
			
			return redirect('exhibitors', year)
	
	else:
		form = None
	
	return render(request, 'exhibitors/create.html', {
		'fair': fair,
		'form': form
	})



def exhibitor(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	
	if not user_can_modify_exhibitor(request.user, exhibitor): return HttpResponseForbidden()
	
	CompanyForm = modelform_factory(Company, fields = '__all__')
	
	if request.user.has_perm('exhibitors.change_exhibitor'):
		# pass the FILES, because the form has a picture
		exhibitor_form = ExhibitorFormFull(request.POST or None, request.FILES or None, instance=exhibitor)
	else:
		exhibitor_form = ExhibitorFormPartial(request.POST or None, request.FILES or None, instance=exhibitor)
	company_form = CompanyForm(request.POST or None, instance=exhibitor.company)
	
	if request.POST and exhibitor_form.is_valid() and company_form.is_valid():
		exh = exhibitor_form.save(commit=False)
		exh.save()
		company_form.save()
		
		return redirect('exhibitors', fair.year)
	
	users = [(recruitment_application.user, recruitment_application.delegated_role) for recruitment_application in RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]
	
	if request.user.has_perm('exhibitors.change_exhibitor'): exhibitor_form.fields['hosts'].choices = [('', '---------')] + [(user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for user in users]
	
	orders = []
	
	for order in Order.objects.filter(purchasing_company = exhibitor.company, product__revenue__fair = fair):
		orders.append({
			'name': order.name if order.name is not None else order.product.name,
			'comment': order.comment,
			'unit_price': order.unit_price if order.unit_price is not None else order.product.unit_price,
			'quantity': order.quantity
		})
	
	return render(request, 'exhibitors/exhibitor.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'exhibitor_form': exhibitor_form,
		'company_form': company_form,
		'contacts': CompanyContact.objects.filter(company = exhibitor.company, active = True),
		'orders': orders
	})


@permission_required('exhibitors.transport')
def exhibitor_transport(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	
	form = TransportForm(request.POST or None, instance = exhibitor)
	
	if request.POST and form.is_valid():
		form.save()
		return redirect('exhibitor', fair.year, exhibitor.pk)
	
	return render(request, 'exhibitors/exhibitor_transport.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'form': form
	})


#Where the user can chose to send email to an exhibitor with their orders
def send_emails(request, year, pk, template_name='exhibitors/send_emails.html'):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)
    no_contact = False
    try:
        contact = CompanyContact.objects.get(exhibitor=exhibitor)
    except:
        no_contact=True
    return render(request, template_name, {'fair': fair, 'exhibitor': exhibitor, 'no_contact': no_contact})

#Comfirmation that email has been sent to the exhibitor
def emails_confirmation(request, year, pk, template_name='exhibitors/emails_confirmation.html'):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    exhibitor = get_object_or_404(Exhibitor, pk=pk)

    fair = get_object_or_404(Fair, year=year)
    return render(request, template_name, {'fair': fair, 'exhibitor': exhibitor})

'''Sends email to exhibitor with their cúrrent orders'''
def send_cr_receipts(request, year, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    fair = get_object_or_404(Fair, year=year)
    exhibitor = get_object_or_404(Exhibitor, pk=pk)
    contact =  CompanyContact.objects.get(exhibitor=exhibitor)

    total_price = 0

    orders_info = []
    #Go thrue orders and get the total price for everything and place the important info as a dictionary in the list orders_info


    send_mail(
        'Your orders for Armada',
        get_template('exhibitors/cr_receipt.html').render(({
            'orders_info' : orders_info,
            'total_price' : total_price,
            'exhibitor_name' : exhibitor.company.name,
            })
        ),
        settings.DEFAULT_FROM_EMAIL,
        [contact.email],
        fail_silently=False)

    return render(request, 'exhibitors/emails_confirmation.html', {'fair': fair, 'exhibitor': exhibitor})


def related_object_form(model, model_name, delete_view_name):
    def view(request, year, exhibitor_pk, instance_pk=None, template_name='exhibitors/related_object_form.html'):
        fair = get_object_or_404(Fair, year=year)
        exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)
        if not user_can_modify_exhibitor(request.user, exhibitor):
            return HttpResponseForbidden()
        instance = model.objects.filter(pk=instance_pk).first()
        FormFactory = modelform_factory(model, exclude=(
        'exhibitor', 'user', 'table_name', 'seat_number', 'ignore_from_placement', 'fair'))
        form = FormFactory(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.exhibitor = exhibitor
            try:
                # Try to put fair to choosen year.
                # If model does not have field just
                # pass and move on
                instance.fair = fair
            except Exception:
                pass
            instance.save()
            return redirect('exhibitor', fair.year,exhibitor_pk)
        delete_url = reverse(delete_view_name, args=(
        fair.year,exhibitor_pk, instance_pk)) if instance_pk != None and delete_view_name != None else None
        return render(request, template_name,
                      {'form': form, 'exhibitor': exhibitor, 'instance': instance, 'model_name': model_name,
                       'delete_url': delete_url, 'fair':fair})

    return view


def related_object_delete(model):
    def view(request, year, exhibitor_pk, instance_pk):
        fair = get_object_or_404(Fair, year=year)
        instance = get_object_or_404(model, pk=instance_pk)
        exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)
        if not user_can_modify_exhibitor(request.user, exhibitor):
            return HttpResponseForbidden()
        instance.delete()
        return redirect('exhibitor', fair.year, exhibitor_pk)

    return view
