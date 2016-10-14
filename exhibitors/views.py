from django.forms import modelform_factory
from django.http import HttpResponseForbidden

from .models import Exhibitor
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.forms import TextInput
from orders.models import Order, Product
from exhibitors.models import Exhibitor
from companies.models import Company


def user_can_modify_exhibitor(user, exhibitor):
	return user.has_perm('exhibitors.change_exhibitor') or user in exhibitor.hosts.all() or user in exhibitor.superiors()


def exhibitors(request, template_name='exhibitors/exhibitors.html'):
	return render(request, template_name, {'exhibitors': Exhibitor.objects.all().order_by('company__name')})


def exhibitor(request, pk, template_name='exhibitors/exhibitor.html'):
	exhibitor = get_object_or_404(Exhibitor, pk=pk)
	if not user_can_modify_exhibitor(request.user, exhibitor):
		return HttpResponseForbidden()

	invoice_fields = ('invoice_reference', 'invoice_reference_phone_number', 'invoice_organisation_name', 'invoice_address',
					  'invoice_address_po_box', 'invoice_address_zip_code', 'invoice_identification', 'invoice_additional_information')

	InvoiceForm = modelform_factory(
		Exhibitor,
		fields=invoice_fields
	)

	transport_to_fair_fields = ('transport_to_fair_type', 'number_of_packages_to_fair', 'number_of_pallets_to_fair', 'estimated_arrival')


	transport_from_fair_fields = ('transport_from_fair_type', 'number_of_packages_from_fair', 'number_of_pallets_from_fair',
								  'transport_from_fair_address', 'transport_from_fair_zip_code','transport_from_fair_recipient_name',
								  'transport_from_fair_recipient_phone_number')


	CompanyForm = modelform_factory(
		Company,
		fields='__all__'
	)

	TransportToFairForm = modelform_factory(
		Exhibitor,
		fields=transport_to_fair_fields,
	)

	TransportFromFairForm = modelform_factory(
		Exhibitor,
		fields=transport_from_fair_fields,
	)

	ExhibitorForm = modelform_factory(
		Exhibitor,
		exclude=('company', 'fair') + invoice_fields + transport_from_fair_fields + transport_to_fair_fields if request.user.has_perm('exhibitors.change_exhibitor') else ('company', 'fair', 'hosts', 'contact') + invoice_fields + transport_from_fair_fields + transport_to_fair_fields,
		widgets={'allergies': TextInput()}

	)


	exhibitor_form = ExhibitorForm(request.POST or None, instance=exhibitor)

	invoice_form = InvoiceForm(request.POST or None, instance=exhibitor)
	transport_to_fair_form = TransportToFairForm(request.POST or None, instance=exhibitor)
	transport_to_fair_form.fields['estimated_arrival'].label = 'Estimaded arrival (format: 2016-12-24 13:37)'

	transport_from_fair_form = TransportFromFairForm(request.POST or None, instance=exhibitor)

	company_form = CompanyForm(request.POST or None, instance=exhibitor.company)

	if exhibitor_form.is_valid() and invoice_form.is_valid() and transport_to_fair_fields.is_valid() and transport_from_fair_form.is_valid() and company_form.is_valid():
		exhibitor_form.save()
		invoice_form.save()
		transport_to_fair_form.save()
		transport_from_fair_form.save()
		company_form.save()
		return redirect('exhibitors')

	users = [(recruitment_application.user, recruitment_application.delegated_role)  for recruitment_application in RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]

	if request.user.has_perm('exhibitors.change_exhibitor'):
		exhibitor_form.fields['hosts'].choices = [('', '---------')] + [(user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for user in users]

	return render(request, template_name, {
		'exhibitor': exhibitor,
		'exhibitor_form': exhibitor_form,
		'invoice_form': invoice_form,
		'transport_to_fair_form': transport_to_fair_form,
		'transport_from_fair_form': transport_from_fair_form,
		'company_form': company_form,
	})

def order(request, exhibitor_pk, order_pk=None, template_name='exhibitors/order_form.html'):
	exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)

	if not user_can_modify_exhibitor(request.user, exhibitor):
		return HttpResponseForbidden()

	OrderFactory = modelform_factory(
		Order,
		exclude=('exhibitor',),
	)
	order = Order.objects.filter(pk=order_pk).first()
	order_form = OrderFactory(request.POST or None, instance=order)

	if order_form.is_valid():
		order = order_form.save(commit=False)
		order.exhibitor = exhibitor
		order.save()
		return redirect('exhibitor', exhibitor_pk)
	return render(request, template_name, {'form': order_form, 'exhibitor': exhibitor, 'order': order})


def order_delete(request, exhibitor_pk, order_pk):
	order = get_object_or_404(Order, pk=order_pk)
	exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)
	if not user_can_modify_exhibitor(request.user, exhibitor):
		return HttpResponseForbidden()
	order.delete()
	return redirect('exhibitor', exhibitor_pk)