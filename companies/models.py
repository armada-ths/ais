from django.db import models
from django.conf import settings
from people.models import Programme

# A 'Contact' is a person working for a 'Company'
class Contact(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            null = True,
            blank = True,
            on_delete=models.CASCADE)
    belongs_to = models.ForeignKey('Company', null=True, related_name="belongs_to", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    alternative_email = models.EmailField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)  # work title, such as CEO or HR.
    work_phone = models.CharField(max_length=200)
    cell_phone = models.CharField(max_length=200, blank=True)
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

    name = models.CharField(max_length=100, verbose_name='Organisation name')
    organisation_number = models.CharField(max_length=100)
    website = models.CharField(max_length=300, blank=True)
    phone_number = models.CharField(max_length=300, blank=True)
    related_programme = models.ManyToManyField(Programme, blank=True)

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

class InvoiceDetails(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='invoice_details')
    reference = models.CharField(max_length=200, blank=True)
    reference_phone_number = models.CharField(max_length=200, blank=True)
    purchase_order_number = models.CharField(max_length=200, blank=True)
    organisation_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    address_po_box = models.CharField(max_length=200, blank=True)
    address_zip_code = models.CharField(max_length=100, blank=True)
    identification = models.CharField(max_length=200, blank=True)
    additional_information = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.reference) + ', ' + str(self.company)


# TODO some model to be able to add a company to sales/sponsorship

# TODO some model to be able to comment on a sale/sponsorship
