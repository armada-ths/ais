from django.db import models
from fair.models import Fair
# Model for company
class Company(models.Model):
    name = models.CharField(max_length=30)
    organisation_number = models.CharField(max_length=30)
    website = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'

# Model for contact person within a company
class CompanyContact(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50) #work title, such as CEO or HR.
    cell_phone = models.CharField(max_length=50)
    work_phone = models.CharField(max_length=50)
    active = models.BooleanField(default=True) #if the contact is active

# Model to be able to add a company to a specific Armada year
class CompanyParticipationYear(models.Model):
    company = models.ForeignKey(Company)
    fair = models.ForeignKey('fair.Fair')


# TODO some model to be able to add a company to sales/sponsorship


# TODO some model to be able to comment on a sale/sponsorship
