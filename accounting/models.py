from django.db import models
from fair.models import Fair

class Revenue(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	fair = models.ForeignKey("fair.Fair", blank = False, on_delete = models.CASCADE)
    
	class Meta:
		verbose_name_plural = "Revenues"
		ordering = ["name"]

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	price = models.PositiveIntegerField(blank = False)
	revenue = models.ForeignKey("Revenue", blank = False, on_delete = models.CASCADE)
	
	class Meta:
		verbose_name_plural = "Products"
		ordering = ["name"]

	def __str__(self):
		return "%s – %s" % (self.revenue, self.name)

# Something that could be sold to CompanyCustomer associated with a Fair
class Invoice(models.Model):
	id_display = models.PositiveIntegerField(blank = False, unique = True)
	company_customer = models.ForeignKey("companies.CompanyCustomer", blank = False, on_delete = models.CASCADE)
	address = models.ForeignKey("companies.CompanyAddress", blank = False, on_delete = models.CASCADE)
	price = models.PositiveIntegerField(blank = False)
	date_issue = models.DateField(blank = False)
	date_due = models.DateField(blank = False)
	date_delivery_start = models.DateField(blank = False)
	date_delivery_end = models.DateField(null = True, blank = True)
	
	class Meta:
		verbose_name_plural = "Invoices"

	def __str__(self):
		return "Invoice " + str(id)

# Something that could be sold to CompanyCustomer associated with a Fair
class ProductOnInvoice(models.Model):
	product = models.ForeignKey(Product, blank = False, on_delete = models.CASCADE)
	invoice = models.ForeignKey(Invoice, blank = False, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100, null = True, blank = True)
	price = models.PositiveIntegerField(null = True, blank = True)
	
	class Meta:
		verbose_name_plural = "Products"
		ordering = ["name"]

	def __str__(self):
		return "%s – %s" % (self.revenue, self.name)
