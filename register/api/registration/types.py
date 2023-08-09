from enum import Enum

from rest_framework import serializers

from django.utils import timezone
from accounting.api import OrderSerializer

from fair.models import Fair
from fair.models import Fair
from companies.models import CompanyContact
from register.models import SignupContract


class RegistrationState(Enum):
    BEFORE_IR = 1
    IR = 2
    AFTER_IR = 3
    CR = 4
    AFTER_CR = 5

    def get(fair: Fair):
        time = timezone.now()

        if time < fair.registration_start_date:
            return RegistrationState.BEFORE_IR
        elif time >= fair.registration_start_date and time < fair.registration_end_date:
            return RegistrationState.IR
        elif (
            time >= fair.registration_end_date
            and time < fair.complete_registration_start_date
        ):
            return RegistrationState.AFTER_IR
        elif (
            time >= fair.complete_registration_start_date
            and time < fair.complete_registration_close_date
        ):
            return RegistrationState.CR
        elif time >= fair.complete_registration_close_date:
            return RegistrationState.AFTER_CR


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


class Registration:
    def __init__(self, type, deadline, company, contact, fair, contract, orders):
        self.type = type
        self.deadline = deadline
        self.company = company
        self.contact = contact
        self.fair = fair
        self.contract = contract
        self.orders = orders


class RegistrationSerializer(serializers.Serializer):
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    contact = ContactSerializer(read_only=True)
    fair = FairSerializer(read_only=True)
    contract = SignupContractSerializer(read_only=True)
    orders = OrderSerializer(many=True)
