import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

from fair.models import Fair
from accounting.models import Revenue, Product
from register.models import SignupLog


# Groups that company customers can be sorted into
class Group(models.Model):
	name = models.CharField(max_length = 100, null = False, blank = False)
	description = models.TextField(blank = True)
	fair = models.ForeignKey(Fair, null = False, blank = False, on_delete = models.CASCADE)
	parent = models.ForeignKey("Group", null = True, blank = True, on_delete = models.CASCADE)
	allow_companies = models.BooleanField(default = True, null = False, blank = False)
	allow_registration = models.BooleanField(default = True, null = False, blank = False)
	allow_responsibilities = models.BooleanField(default = False, null = False, blank = False)
	allow_comments = models.BooleanField(default = False, null = False, blank = False)
	
	def path(self):
		path = [self]
		n = self.parent
		
		while n is not None:
			path.append(n)
			n = n.parent
		
		path.reverse()
		return path
	
	class Meta:
		verbose_name_plural = "Groups"
		ordering = ["parent__name", "name"]
	
	def __str__(self):
		return self.name if self.parent is None else ("%s – %s" % (self.parent, self.name))


# Type of a company, e.g. government agency, company or non-profit organisation
class CompanyType(models.Model):
	type = models.CharField(max_length = 100, null = False, blank = False)
	
	class Meta:
		verbose_name_plural = "Company types"
		ordering = ["type"]

	def __str__(self):
		return self.type


# Represents a company, independent of Fair (see CompanyCustomer below)
class Company(models.Model):
	name = models.CharField(max_length = 100, verbose_name = "Organisation name", unique = True, null = False, blank = False)
	identity_number = models.CharField(max_length = 100, null = True, blank = True)
	website = models.CharField(max_length = 300, null = True, blank = True)
	phone_number = models.CharField(max_length = 200, null = True, blank = True)
	type = models.ForeignKey(CompanyType, null = False, blank = False, on_delete = models.CASCADE)
	modified_by = None
	
	@property
	def addresses(self):
		return CompanyAddress.objects.filter(company = self)
	
	@property
	def log_items(self):
		return CompanyLog.objects.filter(company = self)
	
	@property
	def identity_number_allabolag(self):
		if self.identity_number is not None and re.match("^[0-9]{6}-[0-9]{4}$", self.identity_number):
			return self.identity_number.replace("-", "")
		
		else:
			return None

	class Meta:
		verbose_name_plural = "Companies"
		ordering = ["name"]
		permissions = (("base", "Companies"),)

	def __str__(self):
		return self.name


class CompanyLog(models.Model):
	company = models.ForeignKey(Company, null = False, blank = False, on_delete = models.CASCADE)
	fair = models.ForeignKey(Fair, null = True, blank = True, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(null = False, blank = False, auto_now_add = True)
	data = JSONField()


# Type of a company, e.g. government agency, company or non-profit organisation
class CompanyAddress(models.Model):
	company = models.ForeignKey(Company, null = False, blank = False, on_delete = models.CASCADE)
	
	types = [
		("INVOICE", "Invoice"),
		("TRANSPORT", "Transport"),
		("OFFICE", "Office")
	]
	
	type = models.CharField(max_length = 200, choices = types, null = False, blank = False)
	name = models.CharField(max_length = 200, null = True, blank = True, verbose_name = "Name, if different from the organisation name")
	street = models.CharField(max_length = 200, null = False, blank = False)
	zipcode = models.CharField(max_length = 200, null = False, blank = False)
	city = models.CharField(max_length = 200, null = False, blank = False)
	
	countries = [
		("DENMARK", "Denmark"),
		("FINLAND", "Finland"),
		("FRANCE", "France"),
		("GERMANY", "Germany"),
		("NORWAY", "Norway"),
		("SWEDEN", "Sweden"),
		("UNITED_KINGDOM", "United Kingdom"),
	]
	
	country = models.CharField(max_length = 200, choices = countries, default = "SWEDEN", null = False, blank = False)
	phone_number = models.CharField(max_length = 200, null = True, blank = True)
	email_address = models.CharField(max_length = 200, null = True, blank = True, verbose_name = "E-mail address")
	reference = models.CharField(max_length = 200, null = True, blank = True)
	
	class Meta:
		verbose_name_plural = "Company addresses"

	def __str__(self):
		return self.street + ", " + self.zipcode + " " + self.city


# Connects a Company with a specific Fair, optionally in one or several Group
class CompanyCustomer(models.Model):
	company = models.ForeignKey(Company, null = False, blank = False, on_delete = models.CASCADE)
	fair = models.ForeignKey("fair.Fair", null = False, blank = False, on_delete = models.CASCADE)
	groups = models.ManyToManyField(Group)
	
	@property
	def groups_iterable(self):
		return self.groups.all()
	
	@property
	def responsibles(self):
		return CompanyCustomerResponsible.objects.filter(company_customer = self)
	
	@property
	def comments(self):
		return CompanyCustomerComment.objects.filter(company_customer = self)
	
	@property
	def signatures(self):
		return SignupLog.objects.filter(company = self.company, contract__fair = self.fair)
	
	def get_readonly_fields(self, request, obj = None):
		if obj:
			return ["fair",]
		else:
			return []
	
	class Meta:
		verbose_name_plural = "Company customers"
		ordering = ["company__name"]
		unique_together = ("company", "fair",)

	def __str__(self):
		return "%s at %s" % (self.company, self.fair)


class CompanyCustomerComment(models.Model):
	company_customer = models.ForeignKey(CompanyCustomer, null = False, blank = False, on_delete = models.CASCADE)
	user = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE)
	groups = models.ManyToManyField(Group, blank = True)
	comment = models.TextField(null = False, blank = False)
	timestamp = models.DateTimeField(null = False, blank = False, auto_now_add = True)
	
	@property
	def groups_iterable(self):
		return self.groups.all()
	
	class Meta:
		ordering = ["-timestamp"]
	
	def __str__(self):
		return self.comment


class CompanyCustomerResponsible(models.Model):
	company_customer = models.ForeignKey(CompanyCustomer, null = False, blank = False, on_delete = models.CASCADE)
	group = models.ForeignKey(Group, null = False, blank = False, on_delete = models.CASCADE)
	users = models.ManyToManyField(User, blank = False)
	
	@property
	def users_iterable(self):
		return self.users.all()
	
	class Meta:
		verbose_name_plural = "Company customer responsibles"
		ordering = ["company_customer__company__name", "group__name"]
		unique_together = ("company_customer", "group",)

	def __str__(self):
		return "%s for %s" % (self.group, self.company_customer)


# A "Contact" is a person working for a "Company"
class CompanyContact(models.Model):
	user = models.ForeignKey(User, null = False, blank = False)
	company = models.ForeignKey(Company, null = False, blank = False)
	first_name = models.CharField(max_length = 200, null = True, blank = False, verbose_name = "First name")
	last_name = models.CharField(max_length = 200, null = True, blank = False, verbose_name = "Last name")
	email_address = models.EmailField(max_length = 200, null = False, blank = False, verbose_name = "E-mail address")
	alternative_email_address = models.EmailField(max_length = 200, null = True, blank = True, verbose_name = "Alternative e-mail address")
	title = models.CharField(max_length = 200, null = True, blank = True)
	mobile_phone_number = models.CharField(max_length = 200, null = True, blank = True)
	work_phone_number = models.CharField(max_length = 200, null = True, blank = True)
	active = models.BooleanField(default = True)
	confirmed = models.BooleanField(default = False)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)


@receiver(post_save, sender = Company)
def update_stock(sender, instance, created, **kwargs):
	if created:
		CompanyLog.objects.create(company = instance, data = {"action": "create", "user": instance.modified_by})
	
	else:
		print("company updated by " + str(instance.modified_by))
	
	instance.modified_by = None
