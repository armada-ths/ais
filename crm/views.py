

from rest_framework import viewsets
from .serializers import CompanySerializer


# Import models from companies
from companies.models import Company, CompanyAddress, CompanyCustomerResponsible, Group, CompanyContact, CompanyCustomerComment

class ViewCompanies(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
