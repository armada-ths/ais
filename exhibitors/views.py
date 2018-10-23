from django.http import HttpResponseForbidden
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

from companies.models import Company, CompanyContact, CompanyCustomerComment, CompanyCustomerResponsible
from fair.models import Fair
from accounting.models import Product, Order
from register.models import SignupLog
from banquet.models import Banquet, Participant

from .forms import ExhibitorViewForm, ExhibitorCreateForm, TransportForm, DetailsForm, ContactPersonForm, CommentForm, ExhibitorSearchForm
from .models import Exhibitor, ExhibitorView, LunchTicketDay, LunchTicket


def possible_contact_persons(fair):
	contact_persons = []
	
	for application in RecruitmentApplication.objects.filter(recruitment_period__fair = fair, status = 'accepted', delegated_role__allow_exhibitor_contact_person = True).order_by('recruitment_period', 'user__first_name', 'user__last_name'):
		user = (application.user.pk, application.user)
		added = False
		
		for contact_person in contact_persons:
			if contact_person[0] == application.delegated_role:
				contact_person[1].append(user)
				added = True
				break
		
		if not added: contact_persons.append((application.delegated_role, [user]))
	
	return contact_persons


@permission_required('exhibitors.base')
def exhibitors(request, year, template_name='exhibitors/exhibitors.html'):
	fair = get_object_or_404(Fair, year = year)
	view = ExhibitorView.objects.filter(user = request.user).first()
	
	if not view: view = ExhibitorView(user = request.user).create()
	
	exhibitors = Exhibitor.objects.prefetch_related('contact_persons').filter(fair = fair).order_by('company__name')
	
	form = ExhibitorSearchForm(request.POST or None)
	
	form.fields['contact_persons'].choices = possible_contact_persons(fair)
	
	if request.POST and form.is_valid():
		exhibitors_filtered = []
		
		for exhibitor in exhibitors:
			for contact_person in form.cleaned_data['contact_persons']:
				if contact_person in exhibitor.contact_persons.all():
					exhibitors_filtered.append(exhibitor)
					break
		
		exhibitors = exhibitors_filtered
	
	if not request.user.has_perm('exhibitors.view_all'): exhibitors = [exhibitor for exhibitor in exhibitors if request.user in exhibitor.contact_persons.all()]
	
	return render(request, template_name, {
		'fair': fair,
		'exhibitors': exhibitors,
		'fields': [] if len(view.choices) == 0 else view.choices.split(' '),
		'form': form
	})


@permission_required('exhibitors.base')
def edit_view(request, year, template_name='exhibitors/edit_view.html'):
	view = ExhibitorView.objects.filter(user = request.user).first()
	form = ExhibitorViewForm(request.POST or None, instance=view, user = request.user)

	if form.is_valid():
		form.save()
		return redirect('exhibitors', year)

	return render(request, template_name, {
		'form': form,
		'fair': get_object_or_404(Fair, year = year)
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


@permission_required('exhibitors.base')
def exhibitor(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	
	if not request.user.has_perm('exhibitors.view_all') and request.user not in exhibitor.contact_persons.all(): return HttpResponseForbidden()
	
	orders = []
	
	for order in Order.objects.filter(purchasing_company = exhibitor.company, product__revenue__fair = fair):
		orders.append({
			'name': order.name if order.name is not None else order.product.name,
			'comment': order.comment,
			'unit_price': order.unit_price if order.unit_price is not None else order.product.unit_price,
			'quantity': order.quantity
		})
	
	form_comment = CommentForm(request.POST or None)
	
	if request.POST and form_comment.is_valid():
		comment = form_comment.save(commit = False)
		comment.company = exhibitor.company
		comment.user = request.user
		comment.show_in_exhibitors = True
		comment.save()
		form_comment.save()
		
		form_comment = CommentForm()
	
	contact_persons = []
	
	for contact_person in exhibitor.contact_persons.all():
		application = RecruitmentApplication.objects.filter(recruitment_period__fair = fair, user = contact_person, status = 'accepted').first()
		
		contact_persons.append({
			'user': contact_person,
			'role': application.delegated_role if application is not None else None
		})
	
	for responsible in CompanyCustomerResponsible.objects.select_related('group').filter(company = exhibitor.company, group__fair = fair):
		for user in responsible.users.all():
			application = RecruitmentApplication.objects.filter(recruitment_period__fair = fair, user = user, status = 'accepted').first()
			
			already_found = False
			
			for contact_person in contact_persons:
				if contact_person['user'] == user:
					already_found = True
					break
			
			if not already_found:
				contact_persons.append({
					'user': user,
					'role': application.delegated_role if application is not None else None
				})
	
	lunch_tickets_count_ordered = 0
	
	for order in Order.objects.filter(purchasing_company = exhibitor.company, product = exhibitor.fair.product_lunch_ticket):
		lunch_tickets_count_ordered += order.quantity
	
	lunch_tickets_days = []
	lunch_tickets_count_created = 0
	
	for day in LunchTicketDay.objects.filter(fair = fair):
		lunch_tickets = LunchTicket.objects.filter(exhibitor = exhibitor, day = day)
		lunch_tickets_count_created += len(lunch_tickets)
		
		lunch_tickets_days.append({
			'name': day.name,
			'lunch_tickets': lunch_tickets
		})
	
	banquets = []
	banquet_tickets_count_ordered = 0
	banquet_tickets_count_created = 0
	
	for banquet in Banquet.objects.filter(fair = fair):
		if banquet.product is not None:
			for order in Order.objects.filter(purchasing_company = exhibitor.company, product = banquet.product):
				banquet_tickets_count_ordered += order.quantity
		
		banquet_tickets = Participant.objects.filter(banquet = banquet, company = exhibitor.company)
		banquet_tickets_count_created += len(banquet_tickets)
		
		banquets.append({
			'banquet': banquet,
			'banquet_tickets': banquet_tickets
		})
	
	return render(request, 'exhibitors/exhibitor.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'contacts': CompanyContact.objects.filter(company = exhibitor.company, active = True),
		'orders': orders,
		'comments': CompanyCustomerComment.objects.filter(company = exhibitor.company, show_in_exhibitors = True),
		'form_comment': form_comment,
		'contact_persons': contact_persons,
		'lunch_tickets_count_ordered': lunch_tickets_count_ordered,
		'lunch_tickets_count_created': lunch_tickets_count_created,
		'lunch_tickets_days': lunch_tickets_days,
		'banquet_tickets_count_ordered': banquet_tickets_count_ordered,
		'banquet_tickets_count_created': banquet_tickets_count_created,
		'banquets': banquets,
		'deadline_complete_registration': exhibitor.deadline_complete_registration or fair.complete_registration_close_date
	})


@permission_required('exhibitors.modify_transport')
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


@permission_required('exhibitors.modify_details')
def exhibitor_details(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	
	form = DetailsForm(request.POST or None, instance = exhibitor)
	
	if request.POST and form.is_valid():
		form.save()
		return redirect('exhibitor', fair.year, exhibitor.pk)
	
	return render(request, 'exhibitors/exhibitor_details.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'form': form
	})


@permission_required('exhibitors.modify_contact_persons')
def exhibitor_contact_persons(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	
	form = ContactPersonForm(request.POST or None, instance = exhibitor)
	
	form.fields['contact_persons'].choices = possible_contact_persons(fair)
	
	if request.POST and form.is_valid():
		form.save()
		return redirect('exhibitor', fair.year, exhibitor.pk)
	
	return render(request, 'exhibitors/exhibitor_contact_persons.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'form': form
	})


@permission_required('exhibitors.base')
def exhibitor_comment_edit(request, year, pk, comment_pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	comment = get_object_or_404(CompanyCustomerComment, company = exhibitor.company, pk = comment_pk, user = request.user)
	
	form = CommentForm(request.POST or None, instance = comment)
	
	if request.POST and form.is_valid():
		form.save()
		return redirect('exhibitor', fair.year, exhibitor.pk)
	
	return render(request, 'exhibitors/exhibitor_comment_edit.html', {
		'fair': fair,
		'exhibitor': exhibitor,
		'form': form
	})


@permission_required('exhibitors.base')
def exhibitor_comment_remove(request, year, pk, comment_pk):
	fair = get_object_or_404(Fair, year = year)
	exhibitor = get_object_or_404(Exhibitor, pk = pk)
	comment = get_object_or_404(CompanyCustomerComment, company = exhibitor.company, pk = comment_pk, user = request.user)
	
	comment.delete()
	
	return redirect('exhibitor', fair.year, exhibitor.pk)
