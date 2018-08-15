from django.forms import Form, CharField, ModelMultipleChoiceField, SelectMultiple

from companies.models import Company

from .models import Order

class GenerateCompanyInvoicesForm(Form):
	text = CharField(required = True, label = 'Text to print on all invoices')
	our_reference = CharField(required = True, initial = 'THS Armada Project Leader')
	
	companies = ModelMultipleChoiceField(
		queryset = Company.objects.all(),
		widget = SelectMultiple(attrs = {'size': 20}),
		required = True,
		label = 'Companies to invoice'
	)
