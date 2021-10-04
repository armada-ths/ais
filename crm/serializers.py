from rest_framework import serializers

from companies.models import Company

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'website', 'general_email_address', 'invoice_city')