from django.test import TestCase, Client
from fair.models import Fair
from django.contrib.auth.models import User
from exhibitors.models import Exhibitor
from companies.models import Company, Contact
from django.test import Client

class BanquetViewTestCase(TestCase):
    def setUp(self):
        self.fair = Fair.objects.create(name="Armada 2017", year=2017, pk=82189128287123, current=True)
        self.test_user = User.objects.create_user(username='test', password='test', email='paperback@writer.se')
        self.test_company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.test_contact = Contact.objects.create(user=self.test_user, belongs_to=self.test_company, name="contact name for testing", email="paperback@writer.com", active=True, confirmed=True)
        self.exhibitor = Exhibitor.objects.create(fair=self.fair, company=self.test_company, contact=self.test_contact, pk=99998876544433311)

    #def test_banquet_view(self):
        client = Client()
        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})
        response = client.get('/fairs/2017/banquet/')
        #not permission, should be redirected
        self.assertEqual(response.status_code, 302)
        response = client.get('/fairs/2017/banquet/attendant/new')
        self.assertEqual(response.status_code, 302)
