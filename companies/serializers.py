from rest_framework import serializers
from .models import Company
from drf_writable_nested import UniqueFieldsMixin


COMPANY_FIELDS = (
    "id",
    "name",
    "identity_number",
    "website",
    "general_email_address",
    "invoice_name",
    "invoice_address_line_1",
    "invoice_address_line_2",
    "invoice_address_line_3",
    "invoice_city",
    "invoice_zip_code",
    "invoice_country",
    "invoice_reference",
    "invoice_email_address",
    "e_invoice",
)


class CompanySerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = COMPANY_FIELDS
