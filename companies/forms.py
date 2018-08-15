import re, datetime

from django.forms import ModelForm, HiddenInput, BaseModelFormSet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from accounting.models import Product, Order
from .models import Company, CompanyAddress, CompanyCustomer, CompanyCustomerResponsible, CompanyContact, CompanyCustomerComment, Group


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		fields = ['name', 'identity_number', 'website', 'type', 'ths_customer_id', 'invoice_name', 'invoice_address_line_1', 'invoice_address_line_2', 'invoice_address_line_3', 'invoice_zipcode', 'invoice_city', 'invoice_country', 'invoice_reference', 'invoice_email_address']


class CompanyAddressForm(ModelForm):
	class Meta:
		model = CompanyAddress
		fields = "__all__"


class GroupForm(ModelForm):
	class Meta:
		model = Group
		fields = "__all__"

	def is_valid(self, group):
		valid = super(GroupForm, self).is_valid()
		
		if not valid:
			return valid
		
		parent = self.cleaned_data.get("parent")
		allow_companies = self.cleaned_data.get("allow_companies")
		allow_registration = self.cleaned_data.get("allow_registration")
		
		if parent is not None and parent == group:
			self.add_error("parent", "The group cannot be its own parent.")
			valid = False
		
		if not allow_companies and allow_registration:
			self.add_error("allow_registration", "Companies must be allowed in order to allow registration.")
			valid = False
		
		return valid
	
	def __init__(self, fair, *args, **kwargs):
		super(GroupForm, self).__init__(*args, **kwargs)
		
		self.initial["fair"] = fair.id
		self.fields["fair"].disabled = True
		self.fields["fair"].widget = HiddenInput()


class BaseCompanyAddressFormSet(BaseModelFormSet):
	def clean(self):
		if any(self.errors):
			return
		
		for form in self.forms:
			pass


class BaseCompanyContactFormSet(BaseModelFormSet):
	def clean(self):
		if any(self.errors):
			return
		
		for form in self.forms:
			pass


class CompanyCustomerResponsibleForm(ModelForm):
	group = forms.ModelChoiceField(queryset = Group.objects.all(), widget = forms.RadioSelect(), required = True)
	users = forms.ModelMultipleChoiceField(queryset = User.objects.all(), widget = forms.CheckboxSelectMultiple(), required = True)
	
	def __init__(self, company, *args, **kwargs):
		super(CompanyCustomerResponsibleForm, self).__init__(*args, **kwargs)
		self.initial["company"] = company.id
		self.fields["company"].disabled = True
		self.fields["company"].widget = HiddenInput()
	
	class Meta:
		model = CompanyCustomerResponsible
		fields = "__all__"

	def is_valid(self):
		valid = super(CompanyCustomerResponsibleForm, self).is_valid()
		
		if not valid:
			return valid
		
		group = self.cleaned_data.get("group")
		
		if not group.allow_responsibilities:
			self.add_error("group", "This group cannot be used for responsibilities.")
			valid = False
			
		return valid


class CompanyCustomerCommentForm(ModelForm):
	# TODO: this needs to be Fair-specific
	groups = forms.ModelMultipleChoiceField(queryset = Group.objects.filter(allow_comments = True), widget = forms.CheckboxSelectMultiple(), required = False)
	
	class Meta:
		model = CompanyCustomerComment
		fields = ("groups", "comment",)


def fix_phone_number(n):
	if n is None: return None
	
	n = n.replace(' ', '')
	n = n.replace('-', '')
	
	if n.startswith("00"): n = "+" + n[2:]
	if n.startswith("0"): n = "+46" + n[1:]
	
	return n


class CompanyContactForm(ModelForm):
	def clean(self):
		super(CompanyContactForm, self).clean()
		
		if "mobile_phone_number" in self.cleaned_data:
			self.cleaned_data["mobile_phone_number"] = fix_phone_number(self.cleaned_data["mobile_phone_number"])
		
		if "work_phone_number" in self.cleaned_data:
			self.cleaned_data["work_phone_number"] = fix_phone_number(self.cleaned_data["work_phone_number"])
		
		if "email_address" in self.cleaned_data and self.cleaned_data["email_address"] is not None:
			self.cleaned_data["email_address"] = self.cleaned_data["email_address"].lower()
		
		return self.cleaned_data
	
	def is_valid(self):
		valid = super(CompanyContactForm, self).is_valid()
		
		if not valid:
			return valid
		
		mobile_phone_number = self.cleaned_data.get("mobile_phone_number")
		work_phone_number = self.cleaned_data.get("work_phone_number")
		
		if mobile_phone_number is not None and not re.match(r'\+[0-9]+$', mobile_phone_number):
			self.add_error("mobile_phone_number", "Must only contain numbers and a leading plus.")
			valid = False
		
		if work_phone_number is not None and not re.match(r'\+[0-9]+$', work_phone_number):
			self.add_error("work_phone_number", "Must only contain numbers and a leading plus.")
			valid = False
			
		return valid
	
	class Meta:
		model = CompanyContact
		fields = "__all__"
		exclude = ("user", "company",)


class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["password1", "password2"]


class CreateCompanyContactForm(ModelForm):
	def clean(self):
		super(CreateCompanyContactForm, self).clean()
		
		if "mobile_phone_number" in self.cleaned_data:
			self.cleaned_data["mobile_phone_number"] = fix_phone_number(self.cleaned_data["mobile_phone_number"])
		
		if "work_phone_number" in self.cleaned_data:
			self.cleaned_data["work_phone_number"] = fix_phone_number(self.cleaned_data["work_phone_number"])
		
		if "email_address" in self.cleaned_data and self.cleaned_data["email_address"] is not None:
			self.cleaned_data["email_address"] = self.cleaned_data["email_address"].lower()
		
		return self.cleaned_data
	
	def __init__(self, *args, **kwargs):
		super(CreateCompanyContactForm, self).__init__(*args, **kwargs)
		self.fields["company"].label = "Company"

	class Meta:
		model = CompanyContact
		fields = "__all__"
		exclude = ("user", "active","confirmed")

	def is_valid(self):
		valid = super(CreateCompanyContactForm, self).is_valid()
		
		if not valid:
			return valid
		
		email_address = self.cleaned_data["email_address"]
		mobile_phone_number = self.cleaned_data.get("mobile_phone_number")
		work_phone_number = self.cleaned_data.get("work_phone_number")
		
		if User.objects.filter(username = email_address).first() != None:
			self.add_error("email_address", "Account already exists")
			return False
		
		if mobile_phone_number is not None and not re.match(r'\+[0-9]+$', mobile_phone_number):
			self.add_error("mobile_phone_number", "Must only contain numbers and a leading plus.")
			valid = False
		
		if work_phone_number is not None and not re.match(r'\+[0-9]+$', work_phone_number):
			self.add_error("work_phone_number", "Must only contain numbers and a leading plus.")
			valid = False
		
		return valid


class CreateCompanyContactNoCompanyForm(CreateCompanyContactForm):
	def __init__(self, *args, **kwargs):
		super(CreateCompanyContactForm, self).__init__(*args, **kwargs)

	class Meta:
		model = CompanyContact
		fields = "__all__"
		exclude = ("user", "active", "confirmed", "company")


class CompanyCustomerStatusForm(forms.Form):
	status = forms.ModelChoiceField(queryset = Group.objects.all(), required = False, label = "Status")


class DateInput(forms.DateInput):
	input_type = 'date'


class StatisticsForm(forms.Form):
	date_from = forms.DateField(widget = DateInput(), )
	date_to = forms.DateField(initial = datetime.date.today, widget = DateInput())


class CompanyNewOrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ('product', 'quantity')
	
	def is_valid(self):
		valid = super(CompanyNewOrderForm, self).is_valid()
		
		if not valid:
			return valid
		
		product = self.cleaned_data['product']
		quantity = self.cleaned_data['quantity']
		
		if quantity < 1:
			self.add_error('quantity', 'Must be a positive integer.')
			return False
		
		if product.max_quantity is not None and quantity > product.max_quantity:
			self.add_error('quantity', 'Must not exceed ' + str(product.max_quantity) + '.')
			return False
		
		return valid


class CompanyEditOrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ('product', 'purchasing_company', 'purchasing_user')
	
	def is_valid(self):
		valid = super(CompanyEditOrderForm, self).is_valid()
		
		if not valid:
			return valid
		
		quantity = self.cleaned_data['quantity']
		
		if quantity < 1:
			self.add_error('quantity', 'Must be a positive integer.')
			return False
		
		if self.instance.product.max_quantity is not None and quantity > self.instance.product.max_quantity:
			self.add_error('quantity', 'Must not exceed ' + str(product.max_quantity) + '.')
			return False
		
		return valid
