from django.test import TestCase
from .models import OrderLog
from companies.models import Company, Contact
from fair.models import Fair
from django.contrib.auth.models import User

# Tests that the view is working
class RegisterViewTestCase(TestCase):
    def test_view(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

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



# Below is old stuff
"""from django.test import Client
from .forms import ExhibitorForm
from exhibitors.models import Exhibitor
from locations.models import Location, Room, Building
from orders.models import Order

class ExhibitorFormTestCase(TestCase):
    def test_exhibitorform_valid(self):
        # non empty values
        location = Location.objects.create(room=Room.objects.create(building=Building.objects.create(name="b")))
        fair_location = Location.objects.create(room=Room.objects.create(building=Building.objects.create(name="fb")))
        transport_from_fair_type = "self_transport"
        transport_to_fair_type = "external_transport"



        form_data = {
            'location': location,
            'fair_location': fair_location,
            'transport_from_fair_type': transport_from_fair_type,
            'transport_to_fair_type': transport_to_fair_type,
            'estimated_arrival_of_representatives':'',
            'allergies':'',
            'requests_for_stand_placement':'',
            'heavy_duty_electric_equipment':'',
            'other_information_about_the_stand':'',
            'invoice_reference':'',
            'invoice_reference_phone_number':'',
            'invoice_organisation_name':'',
            'invoice_address':'',
            'invoice_address_po_box':'',
            'invoice_address_zip_code':'',
            'invoice_identification':'',
            'invoice_additional_information':'',
            'number_of_packages_to_fair':0,
            'number_of_pallets_to_fair':0,
            'estimated_arrival':'',
            'number_of_packages_from_fair':0,
            'number_of_pallets_from_fair':0,
            'transport_from_fair_address':'',
            'transport_from_fair_zip_code':'',
            'transport_from_fair_recipient_name':'',
            'transport_from_fair_recipient_phone_number':'',
            'wants_information_about_events':False,
            'wants_information_about_targeted_marketing':False,
            'manual_invoice':False,
            'product_selection':()
        }
        form = ExhibitorForm(data=form_data)
        self.assertTrue(form.is_valid())
"""
