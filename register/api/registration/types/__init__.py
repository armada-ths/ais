from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from util import update_field

from register.api.registration.types.base64image import Base64ImageField

from exhibitors.models import (
    CatalogueCategory,
    CatalogueEmployment,
    CatalogueIndustry,
    CatalogueLocation,
    Exhibitor,
)
from fair.models import Fair
from companies.models import CompanyContact
from register.models import SignupContract

from accounting.api import OrderSerializer


### Didrik (2023) The below serializers could be placed in a more logical
### place, e.g. in the folders of the actual models.


class CheckboxesSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        all_children = self.child.Meta.model.objects.all()
        values = list(data.values_list("id", flat=True))

        return [
            dict(type(self.child)(child).data) | {"selected": child.id in values}
            for child in all_children
        ]


# Use this when serializing a common checkbox model
class CheckboxSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate(self, data):
        try:
            id = int(data["id"])
        except:
            raise serializers.ValidationError("id must be a positive integer")

        try:
            if not self.Meta.model.objects.get(id=id):
                raise
        except:
            raise serializers.ValidationError("item does not exist")

        return super(CheckboxSerializer, self).validate(data)


class ContactSerializer(serializers.ModelSerializer):
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


class FairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fair
        read_only_fields = ("name", "year", "description")
        fields = read_only_fields


class SignupContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupContract
        read_only_fields = ("name", "contract")
        fields = read_only_fields


class CatalogueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogueCategory
        read_only_fields = ("id", "category")
        fields = read_only_fields


class CatalogueIndustrySerializer(CheckboxSerializer):
    class Meta:
        model = CatalogueIndustry
        read_only_fields = ("id", "include_in_form", "industry", "category")
        fields = read_only_fields

    category = CatalogueCategorySerializer


class CatalogueEmploymentSerializer(CheckboxSerializer):
    class Meta:
        model = CatalogueEmployment
        read_only_fields = ("id", "employment", "include_in_form")
        fields = read_only_fields


class CatalogueLocationsSerializer(CheckboxSerializer):
    class Meta:
        model = CatalogueLocation
        read_only_fields = ("id", "location", "include_in_form")
        fields = read_only_fields


class ExhibitorSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Exhibitor
        read_only_fields = (
            "id",
            "deadline_complete_registration",
            "transport_to",
            "transport_from",
            "transport_comment",
        )
        fields = read_only_fields + (
            "transport_information_read",
            "catalogue_about",
            "catalogue_logo_squared",
            "catalogue_logo_freesize",
            "catalogue_contact_name",
            "catalogue_contact_email_address",
            "catalogue_contact_phone_number",
            "catalogue_cities",
            "catalogue_industries",
            "catalogue_employments",
            "catalogue_locations",
        )

    catalogue_logo_squared = Base64ImageField(allow_null=True)
    catalogue_logo_freesize = Base64ImageField(allow_null=True)
    catalogue_industries = CheckboxesSerializer(child=CatalogueIndustrySerializer())
    catalogue_employments = CheckboxesSerializer(child=CatalogueEmploymentSerializer())
    catalogue_locations = CheckboxesSerializer(child=CatalogueLocationsSerializer())

    transport_to = serializers.SerializerMethodField(read_only=True)
    transport_from = serializers.SerializerMethodField(read_only=True)

    def get_transport_to(self, obj):
        return dict(Exhibitor.transport_to_statuses).get(obj.transport_to, "Unknown")

    def get_transport_from(self, obj):
        return dict(Exhibitor.transport_from_statuses).get(
            obj.transport_from, "Unknown"
        )


class RegistrationSerializer(serializers.Serializer):
    # Read only fields
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    has_signed_ir = serializers.SerializerMethodField(read_only=True)
    fair = FairSerializer(read_only=True)
    contract = SignupContractSerializer(read_only=True)

    # Editable fields
    orders = OrderSerializer(many=True)
    contact = ContactSerializer()
    exhibitor = ExhibitorSerializer()

    def update(self, instance, validated_data):
        update_field(instance, validated_data, "exhibitor", ExhibitorSerializer)
        update_field(instance, validated_data, "contact", ContactSerializer)

        return instance

    def get_has_signed_ir(self, obj):
        return obj.ir_signature != None
