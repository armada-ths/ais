from django.test import TestCase, Client
from fair.models import Fair
from exhibitors.models import Exhibitor
from companies.models import Company, Contact
from django.test import Client
from django.contrib.auth.models import User, Group, Permission
from .models import BanquetteAttendant, BanquetTable, BanquetTicket
from .forms import BanquetteAttendantForm
from django.contrib.contenttypes.models import ContentType


class BanquetViewTestCase(TestCase):
    def setUp(self):
        # create basic information for tests
        self.fair = Fair.objects.create(
            name="Armada 2017", year=2017, pk=82189128287123, current=True
        )
        self.test_user = User.objects.create_user(
            username="test", password="test", email="paperback@writer.se"
        )
        self.test_user2 = User.objects.create_user(
            username="test2", password="test2", email="paperback2@writer.se"
        )
        self.test_company = Company.objects.create(
            name="TestCompany1", organisation_type="company"
        )
        self.test_contact = Contact.objects.create(
            user=self.test_user,
            belongs_to=self.test_company,
            name="contact name for testing",
            email="paperback@writer.com",
            active=True,
            confirmed=True,
        )
        self.exhibitor = Exhibitor.objects.create(
            fair=self.fair,
            company=self.test_company,
            contact=self.test_contact,
            pk=99998876544433311,
        )
        # create a group with the banquet view and edit permissions
        self.core_group = Group.objects.create(name="Project Core Team", pk=33333333)
        content_type = ContentType.objects.get_for_model(BanquetteAttendant)
        self.edit_permission = Permission.objects.create(
            content_type=content_type,
            name="banquet_edit_permission",
            codename="banquet_edit_permission",
        )
        self.view_permission = Permission.objects.create(
            content_type=content_type,
            name="banquet_view_permission",
            codename="banquet_view_permission",
        )
        self.core_group.permissions.add(self.edit_permission)
        self.core_group.permissions.add(self.view_permission)

    def test_banquet_view_without_permissions(self):
        """
        Test that not any user can access the banquet attendants view or
        access the page where you create new attendants.
        """
        client = Client()
        response = client.post(
            "/accounts/login/", {"username": "test", "password": "test"}
        )
        response = client.get("/fairs/2017/banquet/")
        # not permission, should get permission denied
        self.assertEqual(response.status_code, 403)
        response = client.get("/fairs/2017/banquet/attendant/new")
        self.assertEqual(response.status_code, 403)

    def test_banquet_view_with_permissions(self):
        """
        Test that users with correct permissions can access
        the banquet attendants view and access the page
        where you create new BanquetteAttendants.
        """
        client = Client()
        self.core_group.user_set.add(self.test_user)

        response = client.post(
            "/accounts/login/", {"username": "test", "password": "test"}
        )

        response = client.get("/fairs/2017/banquet/")
        self.assertEqual(response.status_code, 200)
        response = client.get("/fairs/2017/banquet/attendant/new")
        self.assertEqual(response.status_code, 200)

    def test_banquet_form_not_all_fields(self):
        form_data = {
            "fair": self.fair,
            "first_name": "Cecilia",
            "gender": "female",
            "email": "mail@mail.com",
            "phone_number": "070000000000",
        }
        form = BanquetteAttendantForm(
            data=form_data,
            users=User.objects.all(),
            exhibitors=Exhibitor.objects.all(),
            tables=BanquetTable.objects.all(),
        )
        self.assertFalse(form.is_valid())

    def test_banquet_form_success(self):
        form_data = {
            "fair": self.fair,
            "first_name": "Cecilia",
            "last_name": "Heart",
            "gender": "female",
            "email": "mail@mail.com",
            "phone_number": "070000000000",
        }
        form = BanquetteAttendantForm(
            data=form_data,
            users=User.objects.all(),
            exhibitors=Exhibitor.objects.all(),
            tables=BanquetTable.objects.all(),
        )
        self.assertTrue(form.is_valid())

    def test_banquet_ticket_create(self):
        banquet_ticket1 = BanquetTicket.objects.create(name="Student ticket")
        banquet_ticket2 = BanquetTicket.objects.create(name="Company ticket")
        ticket_query = BanquetTicket.objects.filter(name="Student ticket").first()
        ticket_query_all = BanquetTicket.objects.all()
        self.assertEqual(banquet_ticket1, ticket_query)
        self.assertEqual(len(ticket_query_all), 2)

    def test_banquet_ticket_empty(self):
        banquet_ticket_empty = BanquetTicket.objects.create(name="")
        banquet_ticket_empty = BanquetTicket.objects.create()
        ticket_query = BanquetTicket.objects.all()
        self.assertEqual(len(ticket_query), 2)

    def test_banquet_placement_view(self):
        """
        Test that checks that you will get redirected if
        you have no banquet attendant or are not logged in
        """
        client = Client()
        # no log in, get redirected
        response = client.get("/fairs/2017/banquet/placement")
        self.assertEqual(response.status_code, 302)

        # logged in but no attendant, get redirected
        response = client.post(
            "/accounts/login/", {"username": "test2", "password": "test2"}
        )
        response = client.get("/fairs/2017/banquet/placement")
        self.assertEqual(response.status_code, 302)

        BanquetteAttendant.objects.create(
            fair=self.fair,
            user=self.test_user2,
            first_name="f",
            last_name="l",
            phone_number="0000",
            email="test@testerson.com",
            gender="other",
        )
        # logged in with attendant, get status code ok
        response = client.post(
            "/accounts/login/", {"username": "test2", "password": "test2"}
        )
        response = client.get("/fairs/2017/banquet/placement")
        self.assertEqual(response.status_code, 200)


class BanquetPlacementTestCase(TestCase):
    """
    Test specifically banquet placements
    """

    def setUp(self):
        fair = Fair.objects.create(name="Armada 2017", year=2017, current=True)
        user = User.objects.create_user(username="test", password="test")

        self.attendants = [
            BanquetteAttendant.objects.create(
                fair=fair,
                first_name="Attendant",
                last_name=str(i),
                gender="not_specify",
                email="",
                phone_number="",
                confirmed=True,
            )
            for i in range(10)
        ]
        self.attendants.append(
            BanquetteAttendant.objects.create(
                pk=12,
                fair=fair,
                first_name="Attendant",
                last_name="11",
                gender="not_specify",
                email="",
                phone_number="",
            )
        )

    def test_sitting(self):
        client = Client()
        self.assertEqual(len(BanquetteAttendant.objects.all()), 11)
        self.assertEqual(len(BanquetTable.objects.all()), 0)
        response = client.login(username="test", password="test")
        self.assertTrue(response)

        response = client.get("/fairs/2017/banquet/sit_attendants/")
        self.assertEqual(response.status_code, 403)

        self.assertEqual(len(BanquetTable.objects.all()), 0)

        User.objects.get(username="test").user_permissions.add(
            Permission.objects.get(codename="can_seat_attendants")
        )

        response = client.get("/fairs/2017/banquet/sit_attendants/")
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(BanquetTable.objects.all()), 2)
        self.assertEqual(
            BanquetteAttendant.objects.get(pk=4).table, BanquetTable.objects.get(pk=1)
        )
        self.assertFalse(BanquetteAttendant.objects.get(pk=12).table)
