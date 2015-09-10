from django.db import models

# Model for company
class Company(models.Model):
    company_name = models.CharField(max_length=30)
    organisation_number = models.CharField(max_length=30)
    website = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    #fair = models.ForeignKey(Fair) to be implemented, one company should have FK to a fair.

# Model for contact person within a company
class CompanyContact(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50) #work title, such as CEO or HR.
    cell_phone = models.CharField(max_length=50)
    work_phone = models.CharField(max_length=50)
    active = models.BooleanField(default=True) #if the contact is active during this year or not



