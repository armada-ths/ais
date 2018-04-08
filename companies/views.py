from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from companies.models import Company, CompanyAddress, CompanyCustomer, CompanyCustomerResponsible, Group, CompanyContact
from fair.models import Fair
from .forms import CompanyForm, CompanyContactForm, CompanyAddressForm, BaseCompanyAddressFormSet, BaseCompanyContactFormSet, CompanyCustomerForm, CompanyCustomerResponsibleForm, GroupForm, CompanyCustomerCommentForm

def current_fair():
	return get_object_or_404(Fair, current=True)


@permission_required('companies.base')
def companies_list(request, template_name = 'companies/companies_list.html'):
	fair = current_fair()
	companies = Company.objects.all()
	return render(request, template_name, {'fair': fair, 'companies': companies})


@permission_required('companies.base')
def companies_view(request, pk, template_name = 'companies/companies_view.html'):
	fair = current_fair()
	company = get_object_or_404(Company, pk = pk)
	company_customers = CompanyCustomer.objects.filter(company = company)
	company_contacts = CompanyContact.objects.filter(company = company)
	
	return render(request, template_name, {'fair': fair, 'company': company, 'company_customers': company_customers, 'company_contacts': company_contacts})


@permission_required('companies.base')
def companies_form(request, pk = None, template_name = 'companies/companies_form.html'):
	fair = current_fair()
	
	company = Company.objects.filter(pk = pk).first()
	form = CompanyForm(request.POST or None, instance = company, prefix = "form_company")
	CompanyAddressFormSet = inlineformset_factory(Company, CompanyAddress, form = CompanyAddressForm, min_num = 0, extra = 1)
	CompanyContactFormSet = inlineformset_factory(Company, CompanyContact, form = CompanyContactForm, min_num = 0, extra = 0, can_delete = False)
	
	address_formset = CompanyAddressFormSet(request.POST or None, instance = company, prefix = "form_address") if company else None
	contact_formset = CompanyContactFormSet(request.POST or None, instance = company, prefix = "form_contact") if company else None
	
	if request.method == "POST" and form.is_valid(company) and (address_formset is None or (address_formset.is_valid() and contact_formset.is_valid())):
		company = form.save()
		
		if address_formset:
			address_formset.save()
			contact_formset.save()
		
		return redirect('companies_edit', company.pk)
	
	return render(request, template_name, {'fair': fair, 'form': form, 'company': company, 'address_formset': address_formset, 'contact_formset': contact_formset})


def groups_to_tree_list(groups, selected = None):
	groups_tree = {"selected": None, "children": {}}
	
	for group in groups:
		path = group.path()
		
		p = groups_tree
		
		for step in range(len(path)):
			if path[step] not in p["children"]:
				p["children"][path[step]] = {"selected": None if selected is None else path[step] in selected, "children": {}}
			
			p = p["children"][path[step]]
	
	groups_list = tree_to_list(None, groups_tree)
	
	groups_list.pop(0)
	groups_list.pop(0)
	groups_list.pop()
	
	return groups_list


def tree_to_list(k, groups_tree):
	if len(groups_tree['children'].keys()) > 0:
		o = ["open_short", k, "open"]
		
		for child in groups_tree["children"].keys():
			o = o + tree_to_list({"group": child, 'selected': groups_tree["children"][child]["selected"]}, groups_tree["children"][child])
		
		o.append("close")
	
	else:
		o = ["open_short", k, "close_short"]
	
	return o


@permission_required('companies.base')
def companies_customers_list(request, year, template_name = 'companies/companies_customers_list.html'):
	fair = get_object_or_404(Fair, year = year)
	companies_customers = CompanyCustomer.objects.filter(fair = fair)
	groups_list = groups_to_tree_list(Group.objects.filter(fair = fair))
	
	request.POST.fair = [fair.pk]
	
	form = CompanyCustomerForm(fair, companies_customers, request.POST or None)
	
	if form.is_valid():
		form.save()
	
	return render(request, template_name, {'fair': fair, 'companies_customers': companies_customers, 'form': form, 'groups_list': groups_list})


@permission_required('companies.base')
def companies_customers_view(request, year, pk, template_name = 'companies/companies_customers_view.html'):
	fair = get_object_or_404(Fair, year = year)
	company_customer = get_object_or_404(CompanyCustomer, pk = pk)
	company_contacts = CompanyContact.objects.filter(company = company_customer.company)
	
	initially_selected = []
	
	for responsible in CompanyCustomerResponsible.objects.filter(company_customer = company_customer):
		if request.user in responsible.users.all():
			initially_selected.append(responsible.group)
	
	form = CompanyCustomerCommentForm(request.POST or None, initial = {"groups": initially_selected})
	
	if request.POST and form.is_valid():
		comment = form.save(commit = False)
		comment.company_customer = company_customer
		comment.user = request.user
		comment.save()
		form.save()
		
		form = CompanyCustomerCommentForm()
	
	return render(request, template_name, {'fair': fair, 'company_customer': company_customer, 'company': company_customer.company, 'company_contacts': company_contacts, 'form': form})


@permission_required('companies.base')
def companies_customers_edit(request, year, pk, group_pk = None, responsible_group_pk = None, template_name = 'companies/companies_customers_edit.html'):
	fair = get_object_or_404(Fair, year = year)
	company_customer = get_object_or_404(CompanyCustomer, pk = pk)
	responsibles = CompanyCustomerResponsible.objects.filter(company_customer = company_customer)
	
	if group_pk is not None:
		group_toggle = get_object_or_404(Group, pk = group_pk)
		
		if group_toggle in company_customer.groups.all():
			company_customer.groups.remove(group_toggle)
		
		elif group_toggle.allow_companies:
			company_customer.groups.add(group_toggle)
		
		company_customer.save()
	
	groups_list = groups_to_tree_list(Group.objects.filter(fair = fair), company_customer.groups.all())
	
	if responsible_group_pk is not None:
		responsible_group = get_object_or_404(Group, pk = responsible_group_pk)
		responsible = get_object_or_404(CompanyCustomerResponsible, company_customer = company_customer, group = responsible_group)
	
	else:
		responsible = None
	
	form_responsible = CompanyCustomerResponsibleForm(company_customer, request.POST or None, instance = responsible)
	
	if request.POST and form_responsible.is_valid():
		form_responsible.save()
		return redirect('companies_customers_edit', fair.year, company_customer.pk)
	
	return render(request, template_name, {'fair': fair, 'company_customer': company_customer, 'company': company_customer.company, 'groups_list': groups_list, 'responsibles': responsibles, 'form_responsible': form_responsible, 'responsible': responsible})


@permission_required('companies.base')
def companies_customers_groups(request, year, pk = None, template_name = 'companies/companies_customers_groups.html'):
	fair = get_object_or_404(Fair, year = year)
	groups_list = groups_to_tree_list(Group.objects.filter(fair = fair))
	
	group = Group.objects.filter(pk = pk).first()
	
	form = GroupForm(fair, request.POST or None, instance = group)
	
	if request.POST and form.is_valid(group):
		group = form.save()
		return redirect('companies_customers_groups_edit', fair.year, group.pk)
	
	return render(request, template_name, {'fair': fair, 'groups_list': groups_list, 'form': form, 'form_group': group})
