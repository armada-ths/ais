from django import forms

from companies.models import Company

from .models import Order

class GenerateCompanyInvoicesForm(forms.Form):
	text = forms.CharField(required = True, label = 'Text to print on all invoices')
	our_reference = forms.CharField(required = True, initial = 'THS Armada Project Manager')
	companies = forms.ModelMultipleChoiceField(queryset = Company.objects.all(), widget = forms.SelectMultiple(attrs = {'size': 20}), required = True, label = 'Companies to invoice')
	mark_exported = forms.BooleanField(required = False, label = 'Mark the exported orders as invoiced')


class CompanyCustomerIdForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['ths_customer_id']


class BaseCompanyCustomerIdFormSet(forms.BaseFormSet):
	pass
