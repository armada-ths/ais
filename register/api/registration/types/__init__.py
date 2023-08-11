from rest_framework import serializers

from exhibitors.models import Exhibitor
from fair.models import Fair
from companies.models import CompanyContact
from register.api.registration.types.base64image import Base64ImageField
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



class ExhibitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibitor
        read_only_fields = ("id",)
        fields = read_only_fields + (
            "catalogue_about",
            "catalogue_logo_squared",
            "catalogue_logo_freesize",
            "catalogue_contact_name",
            "catalogue_contact_email_address",
            "catalogue_contact_phone_number",
            # "catalogue_industries",
            # "catalogue_employments",
            # "catalogue_locations",
            # "catalogue_cities",
        )

    catalogue_logo_squared = Base64ImageField(allow_null=True)
    catalogue_logo_freesize = Base64ImageField(allow_null=True)


class RegistrationSerializer(serializers.Serializer):
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    contact = ContactSerializer(read_only=True)
    fair = FairSerializer(read_only=True)
    contract = SignupContractSerializer(read_only=True)
    orders = OrderSerializer(many=True)
    exhibitor = ExhibitorSerializer()

    def update(self, instance, validated_data):
        exhibitor = validated_data.pop("exhibitor", None)
        if exhibitor != None:
            exhibitor_serializer = ExhibitorSerializer(
                instance.exhibitor, data=exhibitor, partial=True
            )

            print(exhibitor_serializer)

            if exhibitor_serializer.is_valid():
                exhibitor_serializer.save()
            else:
                print('Was not valid', exhibitor_serializer.errors)

        return instance
