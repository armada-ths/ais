from django.db import models
from fair.models import Fair

# Model for company
class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Companies'
    
    name = models.CharField(max_length=30)
    organisation_number = models.CharField(max_length=30)
    website = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    # Might be more elegant to split to separate model
    invoice_address_street = models.CharField(max_length=64, blank=True)
    invoice_address_zip_code = models.CharField(max_length=8, blank=True) 
    invoice_address_city = models.CharField(max_length=32, blank=True) 
    invoice_address_country = models.CharField(max_length=32, blank=True) 

    delivery_address_street = models.CharField(max_length=64, blank=True)
    delivery_address_zip_code = models.CharField(max_length=8, blank=True) 
    delivery_address_city = models.CharField(max_length=32, blank=True) 
    delivery_address_country = models.CharField(max_length=32, blank=True) 
    
    def __str__(self):
        return self.name


# A 'CompantContact' is a person working for a 'Company'
class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50) #work title, such as CEO or HR.
    cell_phone = models.CharField(max_length=50)
    work_phone = models.CharField(max_length=50)
    active = models.BooleanField(default=True) #if the contact is active

    def __str__(self):
        return self.name


# An Exhibitor is a 'Company' perticipating in a specific 'Fair'
class Exhibitor(models.Model):
    company = models.ForeignKey(Company)
    fair = models.ForeignKey('fair.Fair')


# TODO some model to be able to add a company to sales/sponsorship


# TODO some model to be able to comment on a sale/sponsorship
