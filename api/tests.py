from http import HTTPStatus

from django.test import TestCase, RequestFactory

from companies.models import Company
from .serializers import company_serializer
from .views import exhibitors

class ExhibitorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name='test')

    def test_company_serializer(self):
        self.assertEqual(company_serializer(self.company), {'name':'test'})

    def test_endpoint(self):
        request = self.factory.get('/api/exhibitors/')
        response = exhibitors(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'exhibitors':[{'name':'test'}]})
