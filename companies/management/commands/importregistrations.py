from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify
from companies.models import Company, Contact
from people.models import Programme as Program
from orders.models import Order, Product
from exhibitors.models import Exhibitor, CatalogInfo, \
        WorkField, JobType, Continent, Value
from fair.models import Fair
from urllib.request import urlopen
from urllib.error import HTTPError
from ast import literal_eval
import csv


REGISTRATION_URL = 'http://anmalan.armada.nu'
FAIR_YEAR = 'Armada 2016'

def get_objects_by_name(Model, names):
    objects = []
    for name in names:
        obj, _ = Model.objects.get_or_create(name=name)
        objects.append(obj)
    return objects


def eval_list(string):
    return literal_eval(string) if string else []


class Command(BaseCommand):
    help = 'takes a csv file from anmalan.armada.nu and imports it to database'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        if not options['file']:
            raise CommandError('Please provide a csv file to import')
        csv.register_dialect('semi', delimiter=';')
        with open(options['file']) as file:
            reader = csv.DictReader(
                    file, dialect='semi')
            if not Fair.objects.filter(name=FAIR_YEAR).exists():
                raise CommandError('Fair not found')
            fair = Fair.objects.get(name=FAIR_YEAR)
            for row in reader:
                if not Company.objects.filter(name=row['company_name']).exists():
                    with transaction.atomic():
                        self.stdout.write("importing company %s" % row['company_name'])
                        contact_name = '%s %s' % (
                                row['first_name'], row['last_name'])
                        contact = Contact.objects.create(
                                name=contact_name,
                                email=row['email'],
                                cell_phone=row['cell_phone_number'],
                                work_phone=row['phone_number'],
                                active=True
                                )
                        contact.save()
                        organisation_type = [tuple[0] for tuple in Company.organisation_types if tuple[1] == row['type_of_organisation']][0]
                        print(organisation_type)
                        company = Company.objects.create(
                                name=row['company_name'],
                                organisation_number=row['organisation_identification_number'],
                                organisation_type=organisation_type,
                                additional_address_information=row['additional_address_information'],
                                website=row['webpage'],
                                contact=contact,
                                address_street=row['organisation_address'],
                                address_zip_code=row['zip_postal_code'],
                                address_city=row['city'],
                                address_country=row['country'],
                                )
                        company.save()

                        exhibitor = Exhibitor.objects.create(
                                company=company,
                                fair=fair,
                                contact=contact,
                                invoice_identification=row[
                                    'invoice_identification'],
                                invoice_address=row[
                                    'invoice_address'],
                                invoice_address_zip_code=row[
                                    'invoice_postal_zip_code'],
                                )
                        exhibitor.save()

                        # Catalog Information
                        programs = get_objects_by_name(
                                Program, eval_list(row['programs']))
                        work_fields = get_objects_by_name(
                                WorkField, eval_list(row['fields']))
                        main_work_field, _ = WorkField.objects.get_or_create(name=row['main_field'])
                        job_types = get_objects_by_name(
                                JobType, eval_list(row['offer']))
                        continents = get_objects_by_name(
                                Continent, eval_list(row['continents']))
                        values = get_objects_by_name(
                                Value, eval_list(row['values']))
                        info = CatalogInfo(
                                exhibitor=exhibitor,
                                display_name=row['name_of_the_organisation'].strip(),
                                short_description=row[(
                                    'describe_what_your_organisation_does'
                                    '_in_three_words_or_less')].strip(),
                                description=row['about_the_organisation'].strip(),
                                employees_sweden=row[
                                    'number_of_employees_in_sweden'],
                                employees_world=row[
                                    'number_of_employees_in_total'],
                                countries=row['countries'],
                                website_url=row['webpage'],
                                facebook_url=row['facebook'],
                                twitter_url=row['twitter'],
                                linkedin_url=row['linkedin'],
                                main_work_field=main_work_field,
                                )
                        info.slug = slugify(info.display_name)
                        info.save()

                        # Exhibitor orders

                        """
                        try:
                            with urlopen(REGISTRATION_URL+row['logotype']) as response:
                                if len(row['logotype']) != 0:
                                    info.logo_original.save(row['logotype'], ContentFile(response.read()))
                            with urlopen(REGISTRATION_URL+row['ad']) as response:
                                if len(row['ad']) != 0:
                                    info.ad_original.save(row['ad'], ContentFile(response.read()))
                        except HTTPError:
                            pass
                        """

                        info.programs.add(*programs)
                        info.work_fields.add(*work_fields)
                        info.job_types.add(*job_types)
                        info.continents.add(*continents)
                        info.values.add(*values)
                        info.save()

                company = Company.objects.get(name=row['company_name'])
                exhibitor = Exhibitor.objects.get(company=company, fair=fair)


                # Exhibition area
                if row['base_kit_armada_2015'].strip() == 'THS Armada\'s base kit':
                    product = Product.objects.get_or_create(name='Base kit', fair=fair, price=32200, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['extra_stand_area'].strip() == 'Stand area 4x2 meter':
                    product = Product.objects.get_or_create(name='Extra stand area 4x2 meter', fair=fair, price=6000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['extra_stand_area'].strip() == 'Stand area 5x2 meter':
                    product = Product.objects.get_or_create(name='Extra stand area 5x2 meter', fair=fair, price=12000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['extra_stand_area'].strip() == 'Stand area 6x2 meter':
                    product = Product.objects.get_or_create(name='Extra stand area 6x2 meter', fair=fair, price=18000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['extra_stand_area'].strip() == 'Stand area 7x2 meter':
                    product = Product.objects.get_or_create(name='Extra stand area 7x2 meter', fair=fair, price=24000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['height_of_stand'].strip() == '2,31 meters to 3,30 meters':
                    product = Product.objects.get_or_create(name='Extra stand height (2,31m - 3,30m)', fair=fair, price=1000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                if row['height_of_stand'].strip() == '3,31 meters or higher':
                    product = Product.objects.get_or_create(name='Extra stand height (3,31m or higher)', fair=fair, price=2000, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)

                # Additional
                for day in [1,2]:
                    number_of_lunches = int(row['number_of_lunches_day_%d' % day])
                    if number_of_lunches > 0:
                        product = Product.objects.get_or_create(name='Lunch tickets day %d' % day, fair=fair, price=125, coa_number=3250)[0]
                        Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_lunches)


                number_of_parking_tickets = int(row['number_of_parking_tickets'] or '0')
                if number_of_parking_tickets > 0:
                    product = Product.objects.get_or_create(name='Parking tickets (Valid for 24h)', fair=fair, price=90, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_parking_tickets)

                number_of_electrical_outlets = int(row['number_of_electrical_outlets'] or '0')
                if number_of_electrical_outlets > 0:
                    product = Product.objects.get_or_create(name='Electrical outlet', fair=fair, price=0, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_electrical_outlets)

                number_of_three_phase_electrical_outlets = int(row['number_of_three_phase_electrical_outlets'] or '0')
                if number_of_three_phase_electrical_outlets > 0:
                    product = Product.objects.get_or_create(name='Three-phase electrical outlet', fair=fair, price=500, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_three_phase_electrical_outlets)

                # Banquet
                try:
                    number_of_banquet_tickets = int(row['number_of_banquet_tickets'] or '0')
                    if number_of_banquet_tickets > 0:
                        product = Product.objects.get_or_create(name='Banquet ticket', fair=fair, price=1100, coa_number=3511)[0]
                        Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_banquet_tickets)
                except ValueError:
                    print('Bad value')

                try:
                    number_of_student_tickets_to_the_banquet = int(row['number_of_student_tickets_to_the_banquet'])
                    if number_of_student_tickets_to_the_banquet > 0:
                        product = Product.objects.get_or_create(name='Banquet ticket student', fair=fair, price=1100, coa_number=3511)[0]
                        Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=number_of_student_tickets_to_the_banquet)
                except ValueError:
                    print('Bad value')


                try:
                    number_of_drink_coupons = int(row['number_of_drink_coupons'])
                    if number_of_drink_coupons > 0:
                        product = Product.objects.get_or_create(name='Drink coupons', fair=fair, price=75, coa_number=3511)[0]
                        Order.objects.get_or_create(exhibitor=exhibitor, product=product,
                                                    amount=number_of_drink_coupons)
                except ValueError:
                    print('Bad value')


                # Additional marketing
                if row['campus_competence'].strip() == 'Standard ad (One ad)':
                    product = Product.objects.get_or_create(name='Campus Competence (Standard)', fair=fair, price=2500, coa_number=3250)[0]
                    Order.objects.get_or_create(exhibitor=exhibitor, product=product, amount=1)
