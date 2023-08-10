from rest_framework import serializers
from rest_framework.fields import (
    empty
)

from django.utils import timezone
from accounting.models import Order
from companies.serializers import CompanySerializer

from fair.models import Fair, RegistrationState
from companies.models import CompanyContact
from register.models import SignupContract, SignupLog

from accounting.api import OrderSerializer
from register.views import get_contract


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_contract_signature(company, fair):
    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type="COMPLETE"
    ).first()

    if signature:
        contract = signature.contract
    else:
        contract = get_contract(company, fair, "COMPLETE")

    return (contract, signature)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = ("first_name", "last_name")


class FairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fair
        fields = ("name", "year", "description")


class SignupContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupContract
        fields = ("name", "contract")


class RegistrationSerializer(serializers.Serializer):
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    contact = ContactSerializer(read_only=True)
    fair = FairSerializer(read_only=True)
    contract = SignupContractSerializer(read_only=True)
    orders = OrderSerializer(many=True)


# Todo 2023 (Didrik Munther): find out which fields should be read only in the IR serializer
class CompanyCRSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)


# We're in CR, the company has picked products and submitted.
# This serializer allows a sales person to change all variables still.
class CompanyCRSubmittedForSalesCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)


# We're in CR, the company has picked products and submitted.
# This serializer disallows a company representative to change all invoice variables.
class CompanyCRSubmittedForPersonCompanySerializer(CompanySerializer):
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


class RegistrationCRSerializer(RegistrationSerializer):
    company = CompanyCRSerializer()

    def update(self, instance, validated_data):
        company = validated_data.pop("company", None)
        if company:
            company_serializer = CompanyCRSerializer(
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

        return instance


class Registration:
    def __init__(self, company, exhibitor, contact, fair, contract, orders):
        self.company = company
        self.exhibitor = exhibitor
        self.contact = contact
        self.fair = fair
        self.contract = contract
        self.orders = orders

        period = fair.get_period()

        if period == RegistrationState.BEFORE_IR:
            pass
        elif period == RegistrationState.IR:
            pass
        elif period == RegistrationState.AFTER_IR:
            pass
        elif period == RegistrationState.CR:
            _, signature = get_contract_signature(company, fair)

            self.deadline = (
                exhibitor.deadline_complete_registration
                or fair.complete_registration_close_date
            )

            if signature != None:
                self.type = "complete_registration_signed"
            else:
                self.type = "complete_registration"
        elif period == RegistrationState.AFTER_CR:
            pass
        else:
            pass

    def get_serializer(self, data=empty, context={}):
        # period = self.fair.get_period()
        return RegistrationCRSerializer(
            self,
            data=data,
            partial=True,
            context=context,
        )
