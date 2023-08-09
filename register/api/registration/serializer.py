from companies.serializers import CompanySerializer


# Todo 2023 (Didrik Munther): find out which fields should be read only in the IR serializer
class CompanyCRSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        read_only_fields = ("id",)
