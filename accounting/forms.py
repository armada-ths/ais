from django.forms import Form, CharField, ModelMultipleChoiceField, SelectMultiple, ModelForm, BaseFormSet

from companies.models import Company

from .models import Order

class GenerateCompanyInvoicesForm(Form):
	text = CharField(required = True, label = 'Text to print on all invoices')
	our_reference = CharField(required = True, initial = 'THS Armada Project Manager')
	
	companies = ModelMultipleChoiceField(
		queryset = Company.objects.all(),
		widget = SelectMultiple(attrs = {'size': 20}),
		required = True,
		label = 'Companies to invoice'
	)


class CompanyCustomerIdForm(ModelForm):
	class Meta:
		model = Company
		fields = ['ths_customer_id']


class BaseCompanyCustomerIdFormSet(BaseFormSet):
	pass
