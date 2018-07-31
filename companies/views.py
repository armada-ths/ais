from slackclient import SlackClient

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.conf import settings

from companies.models import Company, CompanyAddress, CompanyCustomerResponsible, Group, CompanyContact, CompanyCustomerComment
from fair.models import Fair
from recruitment.models import RecruitmentApplication
from .forms import CompanyForm, CompanyContactForm, CompanyAddressForm, BaseCompanyAddressFormSet, BaseCompanyContactFormSet, CompanyCustomerResponsibleForm, GroupForm, CompanyCustomerCommentForm, StatisticsForm, CompanyCustomerStatusForm, CompanyNewOrderForm, CompanyEditOrderForm
from register.models import SignupContract, SignupLog
from accounting.models import Revenue, Order, Product
from people.models import Profile

def current_fair():
	return get_object_or_404(Fair, current=True)

@permission_required('companies.base')
def companies_slack_call(request, year):
	profile = get_object_or_404(Profile, user = request.user)
	
	phone_number = request.GET["phone_number"].strip()
	phone_number = phone_number.replace("+", "00")
	
	sc = SlackClient(settings.SLACK_KEY)
	
	sc.api_call(
		"chat.postMessage",
		channel = profile.slack_id,
		text = "tel://" + phone_number
	)
	
	return HttpResponse('')


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
		
		return redirect('companies_view', company.pk)
	
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


def has_same_group_and_users(q1, q2):
	if not q1.group.allow_statistics or not q2.group.allow_statistics:
		return True
	
	if q1.group != q2.group:
		return False
	
	for o1 in q1.users.all():
		if o1 not in q2.users.all():
			return False
	
	for o2 in q2.users.all():
		if o2 not in q1.users.all():
			return False
	
	return True


def is_equal(q1, q2):
	for ccr1 in q1:
		found = False
		
		for ccr2 in q2:
			if has_same_group_and_users(ccr1, ccr2):
				found = True
				break
		
		if not found:
			return False
	
	for ccr2 in q2:
		found = False
		
		for ccr1 in q1:
			if has_same_group_and_users(ccr2, ccr1):
				found = True
				break
		
		if not found:
			return False
		
	return True


@permission_required('companies.base')
def statistics(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	form = StatisticsForm(request.POST or None)
	
	contracts = []
	smallest = None
	
	for contract in SignupContract.objects.filter(fair = fair).all():
		signatures_raw = SignupLog.objects.filter(contract = contract).order_by('timestamp')
		signatures = []
		
		i = 0
		rows = 0
		
		for signature in signatures_raw:
			responsibilities = list(CompanyCustomerResponsible.objects.filter(company = signature.company))
			
			if smallest is None or signature.timestamp < smallest:
				smallest = signature.timestamp
			
			add = True
			
			for signature_existing in signatures:
				if is_equal(signature_existing['responsibilities'], responsibilities):
					signature_existing['count'] += 1
					signature_existing['timestamps'].append(
					{
						'timestamp': signature.timestamp,
						'count': signature_existing['count']
					})
					
					add = False
					break
			
			if add:
				signatures.append(
				{
					'i': i,
					'responsibilities': responsibilities,
					'count': 1,
					'timestamps': [
					{
						'timestamp': signature.timestamp,
						'count': 1
					}]
				})
						
				i += 1
			
		rows += len(signatures)
		
		row_length = len(signatures)
		table = []
		
		for j in range(len(signatures)):
			for timestamp in signatures[j]['timestamps']:
				row = {
					'timestamp': timestamp['timestamp'],
					'cells': []
				}
				
				for k in range(row_length):
					row['cells'].append(None)
				
				row['cells'][j] = timestamp['count']
				table.append(row)
			
			j += 1
		
		contracts.append(
		{
			'i': len(contracts),
			'name': contract.name,
			'signatures_count': signatures_raw.count(),
			'rows': rows,
			'signatures': signatures,
			'table': table
		})
	
	form.fields['date_from'].initial = smallest
	
	return render(request, 'companies/statistics.html',
	{
		'fair': fair,
		'contracts': contracts,
		'form': form
	})


@permission_required('companies.base')
def companies_list(request, year):
	fair = get_object_or_404(Fair, year = year)
	companies = Company.objects.prefetch_related('groups')
	
	responsibles_list = list(CompanyCustomerResponsible.objects.select_related('company').select_related('group').filter(group__fair = fair).prefetch_related('users'))
	responsibles = {}
	
	for responsible in responsibles_list:
		o = {'group': responsible.group.name, 'users': responsible.users.all()}
		
		if responsible.company not in responsibles:
			responsibles[responsible.company] = [o]
		
		else:
			responsibles[responsible.company].append(o)
	
	signatures_list = []
	signatures = {}
	
	for contract in SignupContract.objects.filter(fair = fair):
		signatures_list = signatures_list + list(SignupLog.objects.select_related('company').select_related('contract').filter(contract = contract))
	
	for signature in signatures_list:
		if signature.company not in signatures:
			signatures[signature.company] = [signature]
		
		else:
			signatures[signature.company].append(signature)
	
	companies_modified = []
	
	for company in companies:
		companies_modified.append({
			'pk': company.pk,
			'name': company.name,
			'status': None, # TODO: fix status!
			'groups': company.groups.filter(fair = fair),
			'responsibles': responsibles[company] if company in responsibles else None,
			'signatures': signatures[company] if company in signatures else None
		})
	
	return render(request, 'companies/companies_list.html',
	{
		'fair': fair,
		'companies': companies_modified
	})


@permission_required('companies.base')
def companies_view(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	
	initially_selected = []
	
	for responsible in CompanyCustomerResponsible.objects.filter(company = company):
		if request.user in responsible.users.all():
			initially_selected.append(responsible.group)
	
	form_comment = CompanyCustomerCommentForm(request.POST if request.POST.get('save_comment') else None, initial = {"groups": initially_selected})
	
	if request.POST and request.POST.get('save_comment') and form_comment.is_valid():
		comment = form_comment.save(commit = False)
		comment.company = company
		comment.user = request.user
		comment.save()
		form_comment.save()
		
		form_comment = CompanyCustomerCommentForm(initial = {"groups": initially_selected})
	
	return render(request, 'companies/companies_view.html',
	{
		'fair': fair,
		'fairs': Fair.objects.all(),
		'company': company,
		'groups': company.groups.all(),
		'comments': CompanyCustomerComment.objects.filter(company = company),
		'contacts': CompanyContact.objects.filter(company = company),
		'signatures': SignupLog.objects.select_related('contract').filter(company = company, contract__fair = fair),
		'responsibles': CompanyCustomerResponsible.objects.select_related('group').filter(company = company, group__fair = fair),
		'profile': get_object_or_404(Profile, user = request.user),
		'form_comment': form_comment,
		'orders': Order.objects.filter(purchasing_company = company, product__revenue__fair = fair)
	})


@permission_required('companies.base')
def companies_edit_responsibles_remove(request, year, pk, responsible_group_pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	responsible_group = get_object_or_404(Group, pk = responsible_group_pk, fair = fair)
	responsible = get_object_or_404(CompanyCustomerResponsible, company = company, group = responsible_group)
	
	responsible.delete()
	
	return redirect('companies_edit', fair.year, company.pk)


@permission_required('companies.base')
def companies_edit(request, year, pk, group_pk = None, responsible_group_pk = None):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	responsibles = CompanyCustomerResponsible.objects.select_related('group').filter(company = company, group__fair = fair)
	
	if group_pk is not None:
		group_toggle = get_object_or_404(Group, pk = group_pk, fair = fair)
		
		if group_toggle in company.groups.all():
			company.groups.remove(group_toggle)
		
		elif group_toggle.allow_companies:
			company.groups.add(group_toggle)
		
		company.save()
	
	groups_list = groups_to_tree_list(Group.objects.filter(fair = fair), company.groups.all())
	
	if responsible_group_pk is not None:
		responsible_group = get_object_or_404(Group, pk = responsible_group_pk, fair = fair)
		responsible = get_object_or_404(CompanyCustomerResponsible, company = company, group = responsible_group)
	
	else:
		responsible = None
	
	form_responsible = CompanyCustomerResponsibleForm(company, request.POST if request.POST.get('save_responsibilities') else None, instance = responsible)
	
	users = [recruitment_application.user for recruitment_application in RecruitmentApplication.objects.filter(status = "accepted", recruitment_period__fair = fair).order_by('user__first_name', 'user__last_name')]
	
	users = [user for user in users if (responsible is not None and user in responsible.users.all()) or user.has_perm('companies.base')]

	form_responsible.fields["users"].choices = [(user.pk, user.get_full_name()) for user in users]
	form_responsible.fields["group"].choices = [(group.pk, group.__str__()) for group in Group.objects.filter(allow_responsibilities = True)]
	
	if request.POST and request.POST.get('save_responsibilities') and form_responsible.is_valid():
		form_responsible.save()
		return redirect('companies_edit', fair.year, company.pk)
	

	form_status = CompanyCustomerStatusForm(request.POST if request.POST.get('save_status') else None, initial = {"status": None}) # TODO: fix
	
	form_status.fields["status"].choices = [('', '---------')] + [(group.pk, group.__str__) for group in Group.objects.filter(fair = fair, allow_status = True)]
	
	if request.POST and request.POST.get('save_status') and form_status.is_valid():
		company.status = form_status.cleaned_data["status"]
		company.save()
	
	return render(request, 'companies/companies_edit.html',
	{
		'fair': fair,
		'company': company,
		'groups_list': groups_list,
		'responsibles': responsibles,
		'responsible': responsible,
		'form_responsible': form_responsible,
		'form_status': form_status
	})


@permission_required('companies.base')
def groups(request, year, pk = None):
	fair = get_object_or_404(Fair, year = year)
	groups_list = groups_to_tree_list(Group.objects.filter(fair = fair))
	
	group = Group.objects.filter(pk = pk).first()
	
	form = GroupForm(fair, request.POST or None, instance = group)
	
	if request.POST and form.is_valid(group):
		group = form.save()
		return redirect('groups_list', fair.year)
	
	return render(request, 'companies/groups.html', {'fair': fair, 'groups_list': groups_list, 'form': form, 'form_group': group})


@permission_required('companies.base')
def companies_comments_edit(request, year, pk, comment_pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	comment = get_object_or_404(CompanyCustomerComment, company = company, pk = comment_pk)
	
	form = CompanyCustomerCommentForm(request.POST or None, instance = comment)
	
	if request.POST and form.is_valid():
		form.save()
		return redirect('companies_view', fair.year, company.pk)
	
	return render(request, 'companies/companies_comments_edit.html',
	{
		'fair': fair,
		'company': company,
		'form': form
	})


@permission_required('companies.base')
def companies_comments_remove(request, year, pk, comment_pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	comment = get_object_or_404(CompanyCustomerComment, company = company, pk = comment_pk)
	
	comment.delete()
	
	return redirect('companies_view', fair.year, company.pk)


@permission_required('companies.base')
def companies_orders_new(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	
	form_order = CompanyNewOrderForm(request.POST or None)
	
	revenues_list = []
	revenues = Revenue.objects.filter(fair = fair)
	
	for revenue in revenues:
		revenue_list = [revenue.name, []]
		
		products = Product.objects.filter(revenue = revenue)
		
		for product in products:
			revenue_list[1].append([product.pk, product.name])
		
		if len(revenue_list[1]) != 0:
			revenues_list.append(revenue_list)
	
	form_order.fields['product'].choices = revenues_list
	
	if request.POST and form_order.is_valid():
		order = form_order.save(commit = False)
		order.purchasing_company = company
		order.save()
		
		return redirect('companies_orders_edit', fair.year, company.pk, order.pk)
	
	return render(request, 'companies/companies_orders_new.html',
	{
		'fair': fair,
		'company': company,
		'form_order': form_order,
		'revenues': revenues_list
	})


@permission_required('companies.base')
def companies_orders_edit(request, year, pk, order_pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	order = get_object_or_404(Order, pk = order_pk, purchasing_company = company)
	
	form_order = CompanyEditOrderForm(request.POST or None, instance = order)
	
	form_order.fields['name'].widget.attrs['placeholder'] = order.product.name
	form_order.fields['quantity'].widget.attrs['max'] = order.product.max_quantity
	form_order.fields['unit_price'].widget.attrs['placeholder'] = order.product.unit_price
	
	if request.POST and form_order.is_valid():
		form_order.save()
		
		return redirect('companies_view', fair.year, company.pk)
	
	return render(request, 'companies/companies_orders_edit.html',
	{
		'fair': fair,
		'company': company,
		'form_order': form_order,
		'product': order.product
	})


@permission_required('companies.base')
def companies_orders_remove(request, year, pk, order_pk):
	fair = get_object_or_404(Fair, year = year)
	company = get_object_or_404(Company, pk = pk)
	order = get_object_or_404(Order, pk = order_pk, purchasing_company = company)
	
	order.delete()
	
	return redirect('companies_view', fair.year, company.pk)
