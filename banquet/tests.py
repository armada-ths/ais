from django.test import TestCase, Client
from fair.models import Fair
from exhibitors.models import Exhibitor
from companies.models import Company, Contact
from django.test import Client
from django.contrib.auth.models import User, Group, Permission
from .models import BanquetteAttendant, BanquetTable
from .forms import BanquetteAttendantForm
from django.contrib.contenttypes.models import ContentType

class BanquetViewTestCase(TestCase):
    def setUp(self):
        # create basic information for tests
        self.fair = Fair.objects.create(name="Armada 2017", year=2017, pk=82189128287123, current=True)
        self.test_user = User.objects.create_user(username='test', password='test', email='paperback@writer.se')
        self.test_company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.test_contact = Contact.objects.create(user=self.test_user, belongs_to=self.test_company, name="contact name for testing", email="paperback@writer.com", active=True, confirmed=True)
        self.exhibitor = Exhibitor.objects.create(fair=self.fair, company=self.test_company, contact=self.test_contact, pk=99998876544433311)
        # create a group with the banquet view and edit permissions
        self.core_group = Group.objects.create(name="Project Core Team",pk=33333333)
        content_type = ContentType.objects.get_for_model(BanquetteAttendant)
        self.edit_permission = Permission.objects.create(content_type=content_type, name="banquet_edit_permission", codename='banquet_edit_permission')
        self.view_permission = Permission.objects.create(content_type=content_type, name="banquet_view_permission",codename='banquet_view_permission')
        self.core_group.permissions.add(self.edit_permission)
        self.core_group.permissions.add(self.view_permission)

    def test_banquet_view_without_permissions(self):
        """
        Test that not any user can access the banquet attendants view or
        access the page where you create new attendants.
        """
        client = Client()
        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})
        response = client.get('/fairs/2017/banquet/')
        #not permission, should get permission denied
        self.assertEqual(response.status_code, 403)
        response = client.get('/fairs/2017/banquet/attendant/new')
        self.assertEqual(response.status_code, 403)

    def test_banquet_view_with_permissions(self):
        """
        Test that users with correct permissions can access
        the banquet attendants view and access the page
        where you create new BanquetteAttendants.
        """
        client = Client()
        self.core_group.user_set.add(self.test_user)

        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})

        response = client.get('/fairs/2017/banquet/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/banquet/attendant/new')
        self.assertEqual(response.status_code, 200)

    def test_banquet_form_not_all_fields(self):
        form_data = {
            'fair': self.fair,
            'first_name': "Cecilia",
            'gender': 'female',
            'email': 'mail@mail.com',
            'phone_number':"070000000000",
            'ticket_type': 'company',
        }
        form = BanquetteAttendantForm(data=form_data, users=User.objects.all(), exhibitors=Exhibitor.objects.all(), tables=BanquetTable.objects.all())
        self.assertFalse(form.is_valid())

    def test_banquet_form_success(self):
        form_data = {
            'fair': self.fair,
            'first_name': "Cecilia",
            'last_name': "Heart",
            'gender': 'female',
            'email': 'mail@mail.com',
            'phone_number':"070000000000",
            'ticket_type': 'company',
        }
        form = BanquetteAttendantForm(data=form_data, users=User.objects.all(), exhibitors=Exhibitor.objects.all(), tables=BanquetTable.objects.all())
        self.assertTrue(form.is_valid())
