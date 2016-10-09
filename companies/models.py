from django.db import models


# A 'Contact' is a person working for a 'Company'
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50)  # work title, such as CEO or HR.
    cell_phone = models.CharField(max_length=50)
    work_phone = models.CharField(max_length=50)
    active = models.BooleanField(default=True)  # if the contact is active

    def __str__(self):
        return self.name


# Model for company
class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=30)
    organisation_number = models.CharField(max_length=30)
    website = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    contact = models.ForeignKey(Contact, null=True, blank=True)

    address_street = models.CharField(max_length=64, blank=True)
    address_zip_code = models.CharField(max_length=8, blank=True)
    address_city = models.CharField(max_length=32, blank=True)
    address_country = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

# TODO some model to be able to add a company to sales/sponsorship

# TODO some model to be able to comment on a sale/sponsorship
