from companies.serializers import CompanySerializer
from dashboard.api.registration.types.serializer import RegistrationSerializer
from util import update_field


class IRCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)


class IRRegistrationSerializer(RegistrationSerializer):
    company = IRCompanySerializer()

    def update(self, instance, validated_data):
        update_field(instance, validated_data, "company", IRCompanySerializer)

        return super().update(instance, validated_data)


class IRBeforeRegistrationSerializer(IRRegistrationSerializer):
    def update(self, instance, validated_data):
        pass
