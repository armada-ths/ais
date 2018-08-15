from django.db import models
from django.contrib.auth.models import User

from fair.models import Fair

class Revenue(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	description = models.CharField(max_length = 100, blank = False)
	fair = models.ForeignKey('fair.Fair', blank = False, on_delete = models.CASCADE)
    
	class Meta:
		verbose_name_plural = 'Revenues'
		ordering = ['fair__year', 'name']
		unique_together = ['name', 'fair']

	def __str__(self): return '%s – %s' % (self.name, self.description)

class Category(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	fair = models.ForeignKey('fair.Fair', blank = False, on_delete = models.CASCADE)
	allow_multiple_purchases = models.BooleanField(default = False)
	
	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['name']
	
	def __str__(self): return self.name

class RegistrationSection(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	description = models.TextField(blank = True, null = True)
	
	class Meta:
		verbose_name_plural = 'Registration sections'
		ordering = ['name']
	
	def __str__(self): return self.name

class Product(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	max_quantity = models.PositiveIntegerField(blank = True, null = True)
	unit_price = models.IntegerField(blank = False)
	revenue = models.ForeignKey(Revenue, blank = False, on_delete = models.CASCADE)
	result_center = models.PositiveIntegerField(blank = False, null = False)
	cost_unit = models.PositiveIntegerField(blank = False, null = False)
	category = models.ForeignKey(Category, blank = True, null = True, on_delete = models.CASCADE)
	description = models.TextField(blank = True)
	registration_section = models.ForeignKey(RegistrationSection, blank = True, null = True, on_delete = models.CASCADE)
	
	class Meta:
		verbose_name_plural = 'Products'
		ordering = ['name']
		permissions = [('base', 'Accounting')]

	def __str__(self): return '%s – %s' % (self.revenue, self.name)

class Order(models.Model):
	product = models.ForeignKey(Product, blank = False, on_delete = models.CASCADE)
	purchasing_company = models.ForeignKey('companies.Company', blank = True, null = True, on_delete = models.CASCADE)
	purchasing_user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100, blank = True, null = True)
	quantity = models.PositiveIntegerField(blank = False)
	unit_price = models.IntegerField(blank = True, null = True)
	comment = models.TextField(blank = True)
	
	class Meta:
		verbose_name_plural = 'Orders'
		ordering = ['name']

	def __str__(self):
		return '%s – %s' % (self.name if self.name is not None else self.product.name, self.purchasing_company.name if self.purchasing_company is not None else self.purchasing_user)

# Something that could be sold to CompanyCustomer associated with a Fair
class Invoice(models.Model):
	id_display = models.PositiveIntegerField(blank = False, unique = True)
	company_customer = models.ForeignKey('companies.CompanyCustomer', blank = False, on_delete = models.CASCADE)
	address = models.ForeignKey('companies.CompanyAddress', blank = False, on_delete = models.CASCADE)
	price = models.PositiveIntegerField(blank = False)
	date_issue = models.DateField(blank = False)
	date_due = models.DateField(blank = False)
	date_delivery_start = models.DateField(blank = False)
	date_delivery_end = models.DateField(null = True, blank = True)
	
	class Meta:
		verbose_name_plural = 'Invoices'

	def __str__(self): return 'Invoice ' + str(id)

# Something that could be sold to CompanyCustomer associated with a Fair
class ProductOnInvoice(models.Model):
	product = models.ForeignKey(Product, blank = False, on_delete = models.CASCADE)
	invoice = models.ForeignKey(Invoice, blank = False, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100, null = True, blank = True)
	price = models.PositiveIntegerField(null = True, blank = True)
	
	class Meta:
		verbose_name_plural = 'Products'
		ordering = ['name']

	def __str__(self): return '%s – %s' % (self.revenue, self.name)
