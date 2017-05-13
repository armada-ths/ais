from django.test import TestCase
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
