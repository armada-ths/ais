import re
from rest_framework import serializers
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

from fair.models import Fair
from accounting.models import Revenue, Product
from register.models import SignupLog, SignupContract
from people.models import Language
import exhibitors


# Groups that company customers can be sorted into
class Group(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    name_full = models.CharField(
        max_length=100, null=False, blank=False, editable=False
    )
    description = models.TextField(blank=True)
    fair = models.ForeignKey(Fair, null=False, blank=False, on_delete=models.CASCADE)
    parent = models.ForeignKey("Group", null=True, blank=True, on_delete=models.CASCADE)
    contract = models.ForeignKey(
        SignupContract, null=True, blank=True, on_delete=models.SET_NULL
    )

    colors = [
        ("BLUE", "Blue"),
        ("GREEN", "Green"),
        ("RED", "Red"),
        ("YELLOW", "Yellow"),
    ]

    color = models.CharField(max_length=200, choices=colors, null=True, blank=True)
    allow_companies = models.BooleanField(default=True, null=False, blank=False)
    allow_registration = models.BooleanField(default=False, null=False, blank=False)
    allow_responsibilities = models.BooleanField(default=False, null=False, blank=False)
    allow_comments = models.BooleanField(default=False, null=False, blank=False)
    allow_statistics = models.BooleanField(default=False, null=False, blank=False)
    allow_status = models.BooleanField(default=False, null=False, blank=False)
    allow_exhibitors = models.BooleanField(default=False, null=False, blank=False)

    def path(self):
        path = [self]
        n = self.parent

        while n is not None:
            path.append(n)
            n = n.parent

        path.reverse()
        return path

    def save(self, *args, **kwargs):
        self.name_full = self.string_path()
        super(Group, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Groups"
        ordering = ["parent__name", "name"]

    def string_path(self):
        return (
            self.name
            if self.parent is None
            else ("%s – %s" % (self.parent.string_path(), self.name))
        )

    def __str__(self):
        return self.name_full


# Type of a company, e.g. government agency, company or non-profit organization
class CompanyType(models.Model):
    type = models.CharField(max_length=100, null=False, blank=False)
    default = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Company types"
        ordering = ["type"]

    def __str__(self):
        return self.type


# Represents a company, independent of Fair (see CompanyCustomer below)
class Company(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Organization name",
        unique=True,
        null=False,
        blank=False,
    )
    identity_number = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=300, null=True, blank=True)
    general_email_address = models.EmailField(
        max_length=200, null=True, blank=True, verbose_name="General e-mail address"
    )
    type = models.ForeignKey(
        CompanyType, null=False, blank=False, on_delete=models.CASCADE
    )
    groups = models.ManyToManyField(Group)
    ths_customer_id = models.CharField(
        max_length=100, verbose_name="THS customer ID", null=True, blank=True
    )
    invoice_name = models.CharField(
        max_length=100, verbose_name="Legal organization name", null=True, blank=True
    )
    invoice_address_line_1 = models.CharField(max_length=300, null=True, blank=True)
    invoice_address_line_2 = models.CharField(max_length=300, null=True, blank=True)
    invoice_address_line_3 = models.CharField(max_length=300, null=True, blank=True)
    invoice_city = models.CharField(max_length=300, null=True, blank=True)
    invoice_zip_code = models.CharField(max_length=300, null=True, blank=True)
    show_externally = models.BooleanField(default=True, null=False, blank=False)

    invoice_country = models.CharField(
        max_length=200, default="SWEDEN", null=True, blank=True
    )
    invoice_reference = models.CharField(max_length=300, null=True, blank=True)
    invoice_email_address = models.EmailField(
        max_length=200, null=True, blank=True, verbose_name="Invoice e-mail address"
    )
    e_invoice = models.BooleanField(default=False)
    e_invoice.help_text = (
        "This attribute should be checked if the company uses e-invoices"
    )
    modified_by = None

    def has_invoice_address(self):
        return (
            (
                self.invoice_address_line_1 is not None
                or self.invoice_address_line_2 is not None
                or self.invoice_address_line_3 is not None
            )
            and self.invoice_zip_code is not None
            and self.invoice_city is not None
            and self.invoice_country is not None
        )

    @property
    def addresses(self):
        return CompanyAddress.objects.filter(company=self)

    @property
    def log_items(self):
        return CompanyLog.objects.filter(company=self)

    @property
    def identity_number_allabolag(self):
        if self.identity_number is not None and re.match(
            "^[0-9]{6}-[0-9]{4}$", self.identity_number
        ):
            return self.identity_number.replace("-", "")

        else:
            return None

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
        permissions = (
            ("base", "Companies"),
            ("host_representative", "Can be host representative"),
        )

    def __str__(self):
        return self.name


class CompanyLog(models.Model):
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE
    )
    fair = models.ForeignKey(Fair, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    data = JSONField()


# Type of a company, e.g. government agency, company or non-profit organization
class CompanyAddress(models.Model):
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE
    )

    types = [("INVOICE", "Invoice"), ("TRANSPORT", "Transport"), ("OFFICE", "Office")]

    type = models.CharField(max_length=200, choices=types, null=False, blank=False)
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Name, if different from the organization name",
    )
    street = models.CharField(max_length=200, null=False, blank=False)
    zipcode = models.CharField(
        max_length=200, null=False, blank=False, verbose_name="Zip code"
    )
    city = models.CharField(max_length=200, null=False, blank=False)

    countries = [
        ("DENMARK", "Denmark"),
        ("FINLAND", "Finland"),
        ("FRANCE", "France"),
        ("GERMANY", "Germany"),
        ("NORWAY", "Norway"),
        ("SWEDEN", "Sweden"),
        ("UNITED_KINGDOM", "United Kingdom"),
    ]

    country = models.CharField(
        max_length=200, choices=countries, default="SWEDEN", null=False, blank=False
    )
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    email_address = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="E-mail address"
    )
    reference = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Your reference"
    )

    class Meta:
        verbose_name_plural = "Company addresses"

    def __str__(self):
        return self.street + ", " + self.zipcode + " " + self.city


# Connects a Company with a specific Fair, optionally in one or several Group
class CompanyCustomer(models.Model):
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE
    )
    fair = models.ForeignKey(
        "fair.Fair", null=False, blank=False, on_delete=models.CASCADE, db_index=True
    )
    status = models.ForeignKey(
        Group, null=True, blank=True, related_name="status", on_delete=models.SET_NULL
    )
    groups = models.ManyToManyField(Group)

    @property
    def responsibles(self):
        return (
            CompanyCustomerResponsible.objects.select_related("group")
            .filter(company_customer=self)
            .prefetch_related("users")
        )

    @property
    def comments(self):
        return CompanyCustomerComment.objects.filter(company_customer=self)

    @property
    def signatures(self):
        return SignupLog.objects.select_related("contract").filter(
            company=self.company, contract__fair=self.fair
        )

    @property
    def exhibitor(self):
        return exhibitors.models.Exhibitor.objects.filter(
            company=self.company, fair=self.fair
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "fair",
            ]
        else:
            return []

    class Meta:
        verbose_name_plural = "Company customers"
        ordering = ["company__name"]
        unique_together = (
            "company",
            "fair",
        )

    def __str__(self):
        return "%s at %s" % (self.company, self.fair)


class CompanyCustomerComment(models.Model):
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE, db_index=True
    )
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    comment = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    show_in_exhibitors = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.comment


class CompanyCustomerResponsible(models.Model):
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE, db_index=True
    )
    group = models.ForeignKey(Group, null=False, blank=False, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=False)

    class Meta:
        verbose_name_plural = "Company customer responsibles"
        ordering = ["company__name", "group__name"]
        unique_together = (
            "company",
            "group",
        )

    def __str__(self):
        return "%s for %s" % (self.group, self.company)


# A "Contact" is a person working for a "Company"
class CompanyContact(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, db_index=True, on_delete=models.SET_NULL
    )
    company = models.ForeignKey(
        Company, null=False, blank=False, on_delete=models.CASCADE
    )
    first_name = models.CharField(
        max_length=200, null=True, blank=False, verbose_name="First name"
    )
    last_name = models.CharField(
        max_length=200, null=True, blank=False, verbose_name="Last name"
    )
    email_address = models.EmailField(
        max_length=200, null=False, blank=False, verbose_name="E-mail address"
    )
    alternative_email_address = models.EmailField(
        max_length=200, null=True, blank=True, verbose_name="Alternative e-mail address"
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=200, null=True, blank=True)
    work_phone_number = models.CharField(max_length=200, null=True, blank=True)
    preferred_language = models.ForeignKey(
        Language, null=True, blank=True, on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(
        default=False,
        verbose_name="This contact has been confirmed to be a real contact in the company",
    )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ["-active", "first_name"]


class CompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = (
            "first_name",
            "last_name",
            "email_address",
            "alternative_email_address",
            "title",
            "mobile_phone_number",
            "work_phone_number",
            "preferred_language",
        )


@receiver(post_save, sender=Company)
def update_stock(sender, instance, created, **kwargs):
    if created:
        CompanyLog.objects.create(
            company=instance, data={"action": "create", "user": instance.modified_by}
        )

    else:
        pass

    instance.modified_by = None
