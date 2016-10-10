from django.forms import modelform_factory
from django.http import HttpResponseForbidden

from .models import Exhibitor
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from orders.models import Order, Product


def exhibitors(request, template_name='exhibitors/exhibitors.html'):
	return render(request, template_name, {'exhibitors': Exhibitor.objects.all().order_by('company__name')})



def exhibitor(request, pk, template_name='exhibitors/exhibitor.html'):
	exhibitor = get_object_or_404(Exhibitor, pk=pk)
	if not request.user.has_perm('exhibitors.change_exhibitor') and request.user not in exhibitor.hosts.all():
		return HttpResponseForbidden()

	ExhibitorForm = modelform_factory(
		Exhibitor,
		exclude=('company', 'fair') if request.user.has_perm('exhibitors.change_exhibitor') else ('company', 'fair', 'hosts', 'contact')
	)
	exhibitor_form = ExhibitorForm(request.POST or None, instance=exhibitor)
	if exhibitor_form.is_valid():
		exhibitor_form.save()
		return redirect('exhibitors')

	users = [(recruitment_application.user, recruitment_application.delegated_role)  for recruitment_application in RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]

	if request.user.has_perm('exhibitors.change_exhibitor'):
		exhibitor_form.fields['hosts'].choices = [('', '---------')] + [(user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for
																		  user in users]

	return render(request, template_name, {
		'exhibitor': exhibitor,
		'exhibitor_form': exhibitor_form
	})


def order(request, exhibitor_pk, order_pk=None, template_name='exhibitors/order_form.html'):
	exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)

	if not request.user.has_perm('exhibitors.change_exhibitor') and request.user not in exhibitor.hosts.all():
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
	if not request.user.has_perm('exhibitors.change_exhibitor') and request.user not in exhibitor.hosts.all():
		return HttpResponseForbidden()
	order.delete()
	return redirect('exhibitor', exhibitor_pk)