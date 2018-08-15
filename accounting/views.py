from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

from fair.models import Fair

from .models import Order
from .forms import GenerateCompanyInvoicesForm

@permission_required('accounting.base')
def accounting(request, year):
	fair = get_object_or_404(Fair, year = year)
	orders = Order.objects.filter(product__revenue__fair = fair).exclude(purchasing_company = None).exclude(unit_price = 0)
	
	companies = []
	
	for order in orders:
		if order.purchasing_company not in companies and order.purchasing_company.has_invoice_address() and order.purchasing_company.ths_customer_id is not None:
			companies.append(order.purchasing_company)
	
	form_generate_company_invoices = GenerateCompanyInvoicesForm(request.POST if request.POST else None, initial = {'text': fair.name})
	
	companies.sort(key = lambda x: x.name)
	form_generate_company_invoices.fields['companies'].choices = [(company.pk, company.name) for company in companies]
	
	txt = None
	
	if request.POST and form_generate_company_invoices.is_valid():
		invoices = []
		
		for company in form_generate_company_invoices.cleaned_data['companies']:
				if company in companies:
					orders_company = []
					
					for order in orders:
						if order.purchasing_company == company:
							orders_company.append(order)
					
					if len(orders_company) != 0:
						invoices.append({
							'company': company,
							'orders': orders_company
						})
		
		txt = 'Rubrik	THS Armada\r\n'
		txt += 'Datumformat	YYYY-MM-DD\r\n'
		
		for invoice in invoices:
			fields_invoice = [''] * 47
			
			fields_invoice[1] = 'Kundfaktura'
			fields_invoice[5] = invoice['company'].ths_customer_id
			fields_invoice[13] = form_generate_company_invoices.cleaned_data['our_reference']
			fields_invoice[15] = 'Faktura ARMADA'
			fields_invoice[16] = form_generate_company_invoices.cleaned_data['text']
			if invoice['company'].invoice_reference is not None and len(invoice['company'].invoice_reference) > 30: fields_invoice[16] += '<CR>Reference: ' + invoice['company'].invoice_reference
			if invoice['company'].invoice_email_address is not None: fields_invoice[16] += '<CR>E-mail address: ' + invoice['company'].invoice_email_address
			if invoice['company'].invoice_reference is not None and len(invoice['company'].invoice_reference) <= 30: fields_invoice[17] = invoice['company'].invoice_reference
			if invoice['company'].invoice_address_line_1 is not None: fields_invoice[26] += invoice['company'].invoice_address_line_1 + '<CR>'
			if invoice['company'].invoice_address_line_2 is not None: fields_invoice[26] += invoice['company'].invoice_address_line_2 + '<CR>'
			if invoice['company'].invoice_address_line_3 is not None: fields_invoice[26] += invoice['company'].invoice_address_line_3 + '<CR>'
			fields_invoice[26] += invoice['company'].invoice_zipcode + ' ' + invoice['company'].invoice_city
			if invoice['company'].invoice_country != 'SWEDEN': fields_invoice[26] += '<CR>' + invoice['company'].get_invoice_country_display()
			if invoice['company'].invoice_name is not None: fields_invoice[27] = invoice['company'].invoice_name
			
			del fields_invoice[0]
			
			txt_orders = []
			
			for order in invoice['orders']:
				fields_order = [''] * 21
				
				fields_order[1] = 'Fakturarad'
				fields_order[2] = '3'
				fields_order[4] = str(order.quantity)
				fields_order[5] = str(order.unit_price if order.unit_price is not None else order.product.unit_price)
				fields_order[8] = order.product.revenue.name
				fields_order[7] = order.name if order.name is not None else order.product.name
				fields_order[12] = 'st'
				fields_order[16] = str(order.product.result_center)
				fields_order[19] = str(order.product.cost_unit)
				
				del fields_order[0]
				
				txt_orders.append('\t'.join(fields_order))
			
			txt += '\t'.join(fields_invoice) + '\r\n'
			for txt_order in txt_orders:
				txt += txt_order + '\r\n'
			txt += 'Kundfaktura-slut\r\n'
		
		form_generate_company_invoices = None
	
	return render(request, 'accounting/accounting.html',
	{
		'fair': fair,
		'form_generate_company_invoices': form_generate_company_invoices,
		'txt': txt
	})
