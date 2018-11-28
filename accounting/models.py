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
		default_permissions = []

	def __str__(self): return '%s – %s' % (self.name, self.description)

class Category(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	fair = models.ForeignKey('fair.Fair', blank = False, on_delete = models.CASCADE)
	allow_multiple_purchases = models.BooleanField(default = False)
	
	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['name']
		default_permissions = []
	
	def __str__(self): return self.name

class RegistrationSection(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	description = models.TextField(blank = True, null = True)
	
	class Meta:
		verbose_name_plural = 'Registration sections'
		ordering = ['name']
		default_permissions = []
	
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
		default_permissions = []
		permissions = [
			('base', 'Accounting'),
			('export_orders', 'Export orders'),
			('ths_customer_ids', 'Edit companies without THS customer IDs')
		]

	def __str__(self): return '%s – %s' % (self.revenue, self.name)


class ExportBatch(models.Model):
	timestamp = models.DateTimeField(blank = False, null = False, auto_now_add = True)
	user = models.ForeignKey(User, blank = False, null = False)
	
	class Meta:
		ordering = ['timestamp']
		default_permissions = []


class Order(models.Model):
	product = models.ForeignKey(Product, blank = False, on_delete = models.CASCADE)
	purchasing_company = models.ForeignKey('companies.Company', blank = True, null = True, on_delete = models.CASCADE)
	purchasing_user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100, blank = True, null = True)
	quantity = models.PositiveIntegerField(blank = False)
	unit_price = models.IntegerField(blank = True, null = True)
	comment = models.TextField(blank = True)
	export_batch = models.ForeignKey(ExportBatch, blank = True, null = True)
	
	class Meta:
		verbose_name_plural = 'Orders'
		ordering = ['name']
		default_permissions = []

	def __str__(self):
		return '%s – %s' % (self.name if self.name is not None else self.product.name, self.purchasing_company.name if self.purchasing_company is not None else self.purchasing_user)
