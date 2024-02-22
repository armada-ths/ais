from django.db import models
from django.db.models import DEFERRED
from django.utils import timezone


# A 'Contact' is a person working for a 'Company'
class SignupContract(models.Model):
    name = models.CharField(max_length=30)
    contract = models.FileField(upload_to="contracts/%Y%m%d/")
    fair = models.ForeignKey("fair.Fair", on_delete=models.CASCADE)
    types = [("INITIAL", "Initial"), ("COMPLETE", "Complete")]
    type = models.CharField(
        max_length=200, choices=types, null=False, blank=False, default=types[0]
    )
    contract_company_type = models.ForeignKey(
        "companies.CompanyType", null=False, blank=False, on_delete=models.CASCADE
    )
    current = models.BooleanField(default=True)
    current.help_text = "Used to determine which contract for a fair, type and company type that should be used if several have been uploaded. Only one contract in this group can be marked as current."
    default = models.BooleanField(default=False)
    default.help_text = "Used to determine which contract for a fair and type that is the default one. Only one contract per fair and type can be marked as current, <strong>make sure one default contract exists before registration opens.</strong>."

    _loaded_values = None

    # These special overrides are meant to prevent anyone from changing an uploaded contract that some companies might already have agreed to
    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):
        if self._loaded_values:
            if (
                self.contract != self._loaded_values["contract"]
                or self.fair.id != self._loaded_values["fair_id"]
            ):
                raise ValueError(
                    "Not allowed to change contract, upload a new one instead!"
                )

        if self.current:
            # set all other contracts for this fair, type and contract_company_type to false to guarantee only one is current
            for contract in SignupContract.objects.filter(
                fair=self.fair,
                type=self.type,
                contract_company_type=self.contract_company_type,
                current=True,
            ):
                if contract != self:
                    contract.current = False
                    contract.save()

        if self.default:
            # set all other contracts for this fair and type to false to guarantee only one is default
            for contract in SignupContract.objects.filter(
                fair=self.fair, type=self.type, default=True
            ):
                if contract != self:
                    contract.default = False
                    contract.save()

        super(SignupContract, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SignupLog(models.Model):
    contract = models.ForeignKey("SignupContract", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        "companies.Company",
        null=True,
        on_delete=models.CASCADE,
        related_name="signature",
    )
    company_contact = models.ForeignKey(
        "companies.CompanyContact", on_delete=models.CASCADE, null=True, blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    types = [
        ("initial", "Initial"),
        ("complete", "Complete"),
    ]

    type = models.CharField(choices=types, null=True, blank=True, max_length=30)

    def get_company_contact_name(self):
        return (
            "-" if self.company_contact == None else self.company_contact.company.name
        )

    def __str__(self):
        return self.get_company_contact_name() + " for " + self.contract.name

    class Meta:
        ordering = [
            "-timestamp",
        ]
