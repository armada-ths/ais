from rest_framework import serializers

from fair.models import Fair
from companies.models import CompanyContact
from register.models import SignupContract

from accounting.api import OrderSerializer


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

