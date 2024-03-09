from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from people.models import Profile
from recruitment.models import RecruitmentApplication

from util import update_field

from dashboard.api.registration.types.base64image import Base64ImageField

from exhibitors.models import (
    CatalogueCategory,
    CatalogueEmployment,
    CatalogueIndustry,
    CatalogueLocation,
    Exhibitor,
)
from fair.models import Fair
from companies.models import CompanyContactSerializer, Group
from register.models import SignupContract

from accounting.api import OrderSerializer, ProductSerializer


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


# Expects a profile object
class SalesCompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "picture_original",
            "phone_number",
            "first_name",
            "last_name",
            "title",
            "email",
        )
        read_only_fields = fields

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_title(self, obj):
        recruitment_application = RecruitmentApplication.objects.filter(
            status="accepted",
            recruitment_period__fair=self.context.get("fair"),
            user=obj.user,
        ).first()

        if recruitment_application is None:
            return None

        return recruitment_application.delegated_role.name

    def get_email(self, obj):
        return obj.armada_email or obj.user.email


class InterestedInSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ("id",)

    def validate(self, data):
        try:
            id = int(data["id"])
            if int(data["id"]) < 0:
                raise
        except:
            raise serializers.ValidationError("id must be a positive integer")

        try:
            if not Group.objects.get(id=id):
                raise
        except:
            raise serializers.ValidationError("group does not exist")

        return data

    def create(self, validated_data):
        group = Group.objects.get(id=validated_data["id"])
        company = self.context["purchasing_company"]
        company.groups.add(group)


class RegistrationSerializer(serializers.Serializer):
    # Read only fields
    type = serializers.StringRelatedField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    fair = FairSerializer(read_only=True)
    ir_contract = SignupContractSerializer(read_only=True)
    cr_contract = SignupContractSerializer(read_only=True)
    sales_contacts = SalesCompanyContactSerializer(read_only=True, many=True)
    products = ProductSerializer(many=True)

    # Editable fields
    orders = OrderSerializer(many=True)
    contact = CompanyContactSerializer()
    exhibitor = ExhibitorSerializer()
    interested_in = InterestedInSerializer(many=True)

    # Add the 'fair' context to sales_contacts
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if "sales_contacts" in ret:
            sales_contacts = SalesCompanyContactSerializer(
                instance=instance.sales_contacts,
                many=True,
                context={"fair": instance.fair, **self.context},
            )

            ret["sales_contacts"] = sales_contacts.data

        return ret

    def update(self, instance, validated_data):
        update_field(instance, validated_data, "contact", CompanyContactSerializer)

        interested_in = validated_data.pop("interested_in", None)
        if interested_in != None:
            serializer = InterestedInSerializer(
                data=interested_in, partial=True, many=True, context=self.context
            )

            if serializer.is_valid():
                company = self.context["purchasing_company"]
                company.groups.clear()
                serializer.create(validated_data=interested_in)

        return instance
