from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify
from companies.models import Company, Contact
from people.models import Programme as Program
from exhibitors.models import Exhibitor, CatalogInfo, \
        WorkField, JobType, Continent, Value
from fair.models import Fair
from urllib.request import urlopen
from urllib.error import HTTPError
from ast import literal_eval
import csv


REGISTRATION_URL = 'http://register.armada.nu'
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
                        company = Company.objects.create(
                                name=row['company_name'],
                                organisation_number=row[
                                    'organisation_identification_number'],
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

                        try:
                            with urlopen(REGISTRATION_URL+row['logotype']) as response:
                                if len(row['logotype']) != 0:
                                    info.logo_original.save(row['logotype'], ContentFile(response.read()))
                            with urlopen(REGISTRATION_URL+row['ad']) as response:
                                if len(row['ad']) != 0:
                                    info.ad_original.save(row['ad'], ContentFile(response.read()))
                        except HTTPError:
                            pass

                        info.programs.add(*programs)
                        info.work_fields.add(*work_fields)
                        info.job_types.add(*job_types)
                        info.continents.add(*continents)
                        info.values.add(*values)
                        info.save()
