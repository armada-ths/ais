from django.db import models
from django.conf import settings


# A 'Contact' is a person working for a 'Company'
class Contact(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            null = True,
            blank = True)
    belongs_to = models.ForeignKey('Company', null=True, blank=True, related_name="belongs_to")
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    alternative_email = models.EmailField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)  # work title, such as CEO or HR.
    cell_phone = models.CharField(max_length=200, blank=True)
    work_phone = models.CharField(max_length=200)
    active = models.BooleanField(default=True)  # if the contact is active
    confirmed = models.BooleanField(default=False)  # (means Armada KAM have confirmed and they are allowed to change company info)
    phone_switchboard = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


# Model for company
class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

    name = models.CharField(max_length=100)
    organisation_number = models.CharField(max_length=100)
    website = models.CharField(max_length=300, blank=True)
    phone_number = models.CharField(max_length=300, blank=True)

    address_street = models.CharField(max_length=200, blank=True)
    address_zip_code = models.CharField(max_length=200, blank=True)
    address_city = models.CharField(max_length=200, blank=True)
    address_country = models.CharField(max_length=200, blank=True)

    additional_address_information = models.CharField(max_length=200, blank=True)


    organisation_types = [
        ('company', 'Company'),
        ('county_council', 'County/County council'),
        ('government_agency', 'Government agency'),
        ('non_profit_organisation', 'Non-profit organisation'),
        ('union', 'Union'),
    ]

    organisation_type = models.CharField(choices=organisation_types, null=True, blank=True, max_length=30)


    def __str__(self):
        return self.name

# TODO some model to be able to add a company to sales/sponsorship

# TODO some model to be able to comment on a sale/sponsorship
