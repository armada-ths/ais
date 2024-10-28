from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError

from companies.models import (
    Company,
    CompanyContact,
    CompanyContactSerializer,
    CompanyType,
)
from companies.serializers import CompanySerializer

from util import status

COMPANY_ALREADY_EXISTS = {
    "err": "company_already_exists",
    "msg": "A company with this name already exists",
}

COMPANY_TYPE_DOES_NOT_EXIST = {
    "err": "company_type_does_not_exist",
    "msg": "This company type does not exist",
}

COMPANY_TYPE_OR_DEFAULT_DOES_NOT_EXIST = {
    "err": "company_type_or_default_does_not_exist",
    "msg": "A company type was not provided, and a default company type does not exists.",
}

EMAIL_ALREADY_IN_USE = {
    "err": "email_address_already_in_use",
    "msg": "This email address is already in use",
}

COMPANY_FIELDS = ["name", "identity_number", "website", "type", "general_email_address"]


class RegisterCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)
        fields = COMPANY_FIELDS


class RegisterCompanyContactSerializer(CompanyContactSerializer):
    class Meta(CompanyContactSerializer.Meta):
        fields = CompanyContactSerializer.Meta.fields + ("company",)


class RegisterSerializer(serializers.Serializer):
    company = RegisterCompanySerializer(allow_null=True)
    contact = RegisterCompanyContactSerializer()
    password = serializers.CharField(
        max_length=128,
    )

    def validate_company(self, data):
        if data is None:
            return data

        errors = {}

        if "name" in data:
            name = data["name"]
            existing_company = Company.objects.filter(name=name).first()
            if existing_company is not None:
                errors["name"] = {
                    **COMPANY_ALREADY_EXISTS,
                    "company_id": existing_company.id,
                }

        if "type" in data:
            company_type_id = data["type"]
            try:
                company_type = CompanyType.objects.get(type=company_type_id)
                data["type"] = company_type
            except CompanyType.DoesNotExist:
                errors["type"] = COMPANY_TYPE_DOES_NOT_EXIST
        else:
            try:
                company_type = CompanyType.objects.get(default=True)
                data["type"] = company_type
            except CompanyType.DoesNotExist:
                errors["type"] = COMPANY_TYPE_OR_DEFAULT_DOES_NOT_EXIST

        if errors:
            raise ValidationError(errors)

        return data

    def validate_contact(self, data):
        email_address = data["email_address"].lower()

        if User.objects.filter(username=email_address).exists():
            raise ValidationError(
                {
                    "email_address": EMAIL_ALREADY_IN_USE,
                }
            )

        return data

    def create(self, validated_data):
        contact_data = validated_data["contact"]
        is_creating_new_company = "company" in validated_data

        if is_creating_new_company:
            try:
                company = Company.objects.create(**validated_data["company"])
            except CompanyType.DoesNotExist:
                raise status.COMPANY_TYPE_DOES_NOT_EXIST

            contact_data["company"] = company

        email_address = contact_data["email_address"].lower()
        password = validated_data["password"]

        user = User.objects.create_user(
            username=email_address,
            email=email_address,
            password=password,
        )

        # If user is creating a new company, the contact is confirmed by default
        CompanyContact.objects.create(
            **contact_data, user=user, confirmed=is_creating_new_company
        )


@require_POST
@csrf_exempt
def create_company_contact(request):
    data = JSONParser().parse(request)
    serializer = RegisterSerializer(
        data=data,
        partial=True,
    )

    if serializer.is_valid():
        try:
            serializer.create(validated_data=serializer.validated_data)
        except ValidationError as e:
            return status.serializer_error(e.detail)
        except Company.DoesNotExist:
            return status.COMPANY_DOES_NOT_EXIST

        user = authenticate(
            username=serializer.validated_data["contact"]["email_address"].lower(),
            password=serializer.validated_data["password"],
        )

        login(request, user)

        return JsonResponse(serializer.data)

    return status.serializer_error(serializer.errors)
