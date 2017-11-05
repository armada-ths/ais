from django.test import TestCase, Client
from .forms import ExhibitorForm
from exhibitors.models import Exhibitor
from .models import OrderLog, SignupContract
from companies.models import Company, Contact
from orders.models import Product, Order, ProductType
from fair.models import Fair
from django.contrib.auth.models import User
from matching.models import Survey, Question, Response, TextAns, ChoiceAns, IntegerAns, BooleanAns
from django.forms import Field

from django.test import Client

# Tests that the view is working
class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.fair = Fair.objects.create(name="Armada 2017", year=2017, pk=82189128287123, current=True)
        self.test_user = User.objects.create_user(username='test', password='test', email='paperback@writer.se')
        self.test_company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.test_contact = Contact.objects.create(user=self.test_user, belongs_to=self.test_company, name="contact name for testing", email="paperback@writer.com", active=True, confirmed=True)

    def test_view(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    # should get redirected if no contact
    """def test_no_contract(self):
        client = Client()
        # log in with test user
        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)

        # should be no contract found 404
        response = client.get('/register/home/')
        self.assertEqual(response.status_code, 404)"""

    """def test_with_contract(self):
        client = Client()

        self.contract = SignupContract.objects.create(name="contract1", contract="hhh", fair=self.fair, current=True)

        # log in with test user
        response = client.post('/accounts/login/', {'username': 'test', 'password': 'test'})

        # test that you will be redirected correctly
        response = client.get('/register/home/')
        self.assertEqual(response.status_code, 302)"""




class OrderLogTestCase(TestCase):
    def test(self):

        fair = Fair.objects.create(name="fair1", year=2017, description="description", current=True)
        fair2 = Fair.objects.create(name="fair2", year=2016, description="description2", current=False)
        user1 = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
        user2 = User.objects.create_user(username='paul',
                                         email='paul@beatles.com',
                                         password='glass onion')

        company = Company.objects.create(name="TestCompany1 for testing", organisation_type='company')
        company2 = Company.objects.create(name="TestCompany1 for testing", organisation_type='company')
        contact = Contact.objects.create(user=user1, belongs_to=company, name="contact name for testing", email="email@hotmail.com", active=True, confirmed=True)
        contact2 = Contact.objects.create(user=user2, belongs_to=company2, name="contact name 2 for testing", email="email2@hotmail.com", active=True, confirmed=True)

        # Create OrderLog
        log0 = OrderLog.objects.create(contact=contact, company=contact.belongs_to, action='save', fair=Fair.objects.get(current=True), products="Test product 1")
        log1 = OrderLog.objects.create(contact=contact, company=contact.belongs_to, action='submit', fair=Fair.objects.get(current=True), products="Test product 1\nTest product 2")
        log2 = OrderLog.objects.create(contact=contact2, company=contact.belongs_to, action='save', fair=Fair.objects.get(year=2016), products="My test products")
        # Get all logs from current fair
        currentLogs = OrderLog.objects.filter(fair=Fair.objects.get(current=True))
        oldLogs = OrderLog.objects.filter(fair=Fair.objects.get(current=False))

        self.assertEqual(log1.action, 'submit')
        self.assertEqual(log2.action, 'save')
        self.assertEqual(log1.products, "Test product 1\nTest product 2")
        self.assertEqual(log2.products, "My test products")
        self.assertEqual(len(currentLogs), 2)
        self.assertEqual(len(oldLogs), 1)



class ExhibitorFormTestCase(TestCase):
    def setUp(self):
        self.fair = Fair.objects.create(name="Armada 2017", year=2017, pk=82189128287123, current=True)
        self.user = User.objects.create_user(username='test', password='test', email='paperback@writer.se')
        self.company = Company.objects.create(name="TestCompany1", organisation_type='company')
        self.contact = Contact.objects.create(user=self.user, belongs_to=self.company, name="contact name for testing", email="paperback@writer.com", active=True, confirmed=True)
        self.contract = SignupContract.objects.create(name="contract1", contract="hhh", fair=self.fair, current=True)
        self.exhibitor = None

        self.banquet_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Banquet"))
        self.lunch_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="AdditionalLunch"))
        self.event_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Events"))
        self.room_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Rooms"))
        self.nova_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Nova"))
        self.stand_area_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Additional Stand Area"))
        self.stand_height_products = Product.objects.filter(fair=self.fair, product_type=ProductType.objects.filter(name="Additional Stand Height"))

        self.current_banquet_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.banquet_products)
        self.current_lunch_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.lunch_products)
        self.current_event_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.event_products)
        self.current_room_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.room_products)
        self.current_nova_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.nova_products)
        self.current_stand_area_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.stand_area_products)
        self.current_stand_height_orders = Order.objects.filter(exhibitor=self.exhibitor, product__in=self.stand_height_products)

        self.matching_survey = Survey.objects.none()
        self.matching_questions = Question.objects.none()
        self.matching_responses = Response.objects.none()

        self.timeFlag, self.time_disp = (None, [None, None])

    def test_exhibitorform_no_answers(self):
        """
        No answers in form, e.g have not accepted contract agreement, should fail.
        """
        form = ExhibitorForm(
            instance = self.exhibitor,
            banquet = self.banquet_products,
            lunch = self.lunch_products,
            events = self.event_products,
            rooms = self.room_products,
            nova = self.nova_products,
            stand_area = self.stand_area_products,
            stand_height = self.stand_height_products,
            banquet_orders = self.current_banquet_orders,
            lunch_orders = self.current_lunch_orders,
            event_orders = self.current_event_orders,
            room_orders = self.current_room_orders,
            nova_orders = self.current_nova_orders,
            stand_area_orders = self.current_stand_area_orders,
            stand_height_orders = self.current_stand_height_orders,
            company = self.company,
            contact = self.contact,
            matching_survey = self.matching_survey,
            matching_questions = self.matching_questions,
            matching_responses = self.matching_responses,
            timeFlag = self.timeFlag,
            time_disp = self.time_disp,
        )
        self.assertFalse(form.is_valid())
