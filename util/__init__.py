import os

from exhibitors.models import Exhibitor

from . import status

from rest_framework import serializers

from django.contrib.auth.models import User
from django.utils import timezone
from companies.models import CompanyContact

from fair.models import Fair
from register.models import SignupLog
from register.views import get_contract

is_dev = os.environ["DJANGO_SETTINGS_MODULE"] == "ais.local.settings"


class JSONError(BaseException):
    def __init__(self, status):
        self.status = status


def get_contract_signature(company, fair, type="COMPLETE"):
    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type=type
    ).first()

    if signature:
        contract = signature.contract
    else:
        contract = get_contract(company, fair, type)

    return (contract, signature)


def get_fair():
    return Fair.objects.filter(year=timezone.now().year).first()


def get_user(request):
    user = request.user
    if not user.is_authenticated:
        if is_dev:
            user = User.objects.filter(email="dashboard@armada.nu").first()
        else:
            return None

    return user


def get_company_contact(user):
    contact = CompanyContact.objects.filter(user=user).exclude(company=None).first()
    if contact == None:
        raise status.USER_HAS_NO_COMPANY

    return contact


def get_exhibitor(company):
    return Exhibitor.objects.filter(fair=get_fair(), company=company).first()


def update_field(
    instance, validated_data, field: str, Serializer: serializers.Serializer
):
    item = validated_data.pop(field, None)
    if item != None:
        serializer = Serializer(getattr(instance, field), data=item, partial=True)

        if serializer.is_valid():
            serializer.save()
