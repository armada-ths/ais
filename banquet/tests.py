from django.test import TestCase, Client
from fair.models import Fair
from django.contrib.auth.models import User
from exhibitors.models import Exhibitor
from django.test import Client

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.fair = Fair.objects.create(name="Armada 2017", year=2017, pk=82189128287123, current=True)
        self.test_user = User.objects.create_user(username='test', password='test', email='paperback@writer.se')
        self.test_company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.test_contact = Contact.objects.create(user=self.test_user, belongs_to=self.test_company, name="contact name for testing", email="paperback@writer.com", active=True, confirmed=True)

    def test_banquet_view(self):
        client = Client()
        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})
        response = self.client.get('/fairs/2017/banquet/')
        self.assertEqual(response.status_code, 200)
