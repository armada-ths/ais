from rest_framework import serializers

from companies.models import Company, CompanyLog

class CompanySerializerLog(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompanyLog
        fields = ('data')

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    
    companyLog = CompanySerializerLog(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('name', 'website', 'general_email_address', 'invoice_city', 'companyLog')



