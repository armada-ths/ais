from accounting.models import Order

from accounting.api import OrderSerializer

from companies.serializers import CompanySerializer
from register.api.registration.types import RegistrationSerializer


class CRCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)


# We're in CR, the company has picked products and submitted.
# This serializer disallows a company representative to change all invoice variables.
class CRSignedCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = (
            "id",
            "identity_number",
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


class CRSignedRegistrationSerializer(RegistrationSerializer):
    company = CRSignedCompanySerializer()

    def update(self, instance, validated_data):
        company = validated_data.pop("company", None)
        if company != None:
            company_serializer = CRSignedCompanySerializer(
                instance.company, data=company, partial=True
            )
            if company_serializer.is_valid():
                company_serializer.save()

        return super().update(instance, validated_data)


class CRRegistrationSerializer(RegistrationSerializer):
    company = CRCompanySerializer()

    def update(self, instance, validated_data):
        company = validated_data.pop("company", None)
        if company != None:
            company_serializer = CRCompanySerializer(
                instance.company, data=company, partial=True
            )
            if company_serializer.is_valid():
                company_serializer.save()

        orders = validated_data.pop("orders", None)
        if orders != None:
            orders_serializer = OrderSerializer(
                data=orders, partial=True, many=True, context=self.context
            )
            if orders_serializer.is_valid():
                # Completely replace the orders with the orders in the request
                Order.objects.filter(
                    purchasing_company=self.context["purchasing_company"]
                ).delete()
                instance.orders = orders_serializer.create(validated_data=orders)

        return super().update(instance, validated_data)
