from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, update_image_field
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
    company = models.ForeignKey('companies.Company')
    fair = models.ForeignKey('fair.Fair')
    hosts = models.ManyToManyField(User, blank=True)
    contact = models.ForeignKey('companies.Contact', null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)

    invoice_identification = models.CharField(max_length=200, blank=True)
    invoice_address = models.CharField(max_length=200, blank=True)
    invoice_address_zip_code = models.CharField(max_length=100, blank=True)
    invoice_address_city = models.CharField(max_length=200, blank=True)
    invoice_address_country = models.CharField(max_length=200, blank=True)

    statuses = [
        ('accepted', 'Accepted'),
        ('registered', 'Registered'),
        ('complete_registration', 'Complete registration'),
        ('contacted_by_host', 'Contacted by host'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked in'),
        ('checked_out', 'Checked out'),
    ]

    status = models.CharField(choices=statuses, null=True, blank=True, max_length=30)
    allergies = models.TextField(null=True, blank=True)
    requests_for_stand_placement = models.CharField(max_length=200, blank=True)
    heavy_duty_electric_equipment = models.CharField(max_length=500, blank=True)
    other_information_about_the_stand = models.CharField(max_length=500, blank=True)



    will_send_goods_to_ths_armadas_goods_reception_before_the_fair = ''

    transport_to_fair_types = [
        ('external_transport', 'Yes, with an external delivery firm'),
        ('arkad_transport', 'Yes, with transport from Arkad in Lund'),
        ('self_transport', 'No, we will bring our goods ourselves'),
    ]
    transport_to_fair_type = models.CharField(choices=transport_to_fair_types, null=True, blank=True, max_length=30)


    transport_from_fair_types = [
        ('third_party_builders_transportation', 'We use a third-party to build our stand who will transport our goods from the fair'),
        ('armada_transportation', 'We use Armada Transport'),
        ('self_transportation', 'We will arrange our own transportation immediately after the fair (note that there is limited access for larger transportation services as the fair closes and it may take some time before your equipment can be picked up)'),
    ]
    transport_from_fair_type = models.CharField(choices=transport_from_fair_types, null=True, blank=True, max_length=300)

    number_of_packages_from_fair = models.IntegerField(default=0)
    number_of_pallets_from_fair = models.IntegerField(default=0)
    number_of_packages_to_fair = models.IntegerField(default=0)
    number_of_pallets_to_fair = models.IntegerField(default=0)

    def total_cost(self):
        return sum([order.price() for order in self.order_set.all()])

    def __str__(self):
        return '%s at %s' % (self.company.name, self.fair.name)


# Work field that an exhibitor operates in
class WorkField(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Job type that an exhibitor offers
class JobType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Continent that an exhibitor operates in
class Continent(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Value or work environment that an exhibitor has
class Value(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Info about an exhibitor to be displayed in apps and on website
class CatalogInfo(models.Model):
    exhibitor = models.OneToOneField(
            Exhibitor,
            on_delete=models.CASCADE,
            )
    display_name = models.CharField(max_length=200)
    slug = models.SlugField(db_index=False, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    employees_sweden = models.IntegerField(default=0)
    employees_world = models.IntegerField(default=0)
    countries = models.IntegerField(default=0)
    website_url = models.CharField(max_length=300, blank=True)
    facebook_url = models.CharField(max_length=300, blank=True)
    twitter_url = models.CharField(max_length=300, blank=True)
    linkedin_url = models.CharField(max_length=300, blank=True)

    # Image fields
    # Field with name ending with original serves as the original uploaded
    # image and should be the only image uploaded,
    # the others are auto generated
    logo_original = models.ImageField(
            upload_to=UploadToDirUUID('exhibitors', 'logo_original'),
            blank=True,
            )
    logo_small = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'logo_small'), blank=True)
    logo = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'logo'), blank=True)

    ad_original = models.ImageField(
            upload_to=UploadToDirUUID('exhibitors', 'ad_original'), blank=True)
    ad = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'ad'), blank=True)

    # ManyToMany relationships
    programs = models.ManyToManyField('people.Programme', blank=True)
    main_work_field = models.ForeignKey(
            WorkField, blank=True, null=True, related_name='+')
    work_fields = models.ManyToManyField(
            WorkField, blank=True, related_name='+')
    job_types = models.ManyToManyField(JobType, blank=True)
    continents = models.ManyToManyField(Continent, blank=True)
    values = models.ManyToManyField(Value, blank=True)

    def __str__(self):
        return self.display_name

    # Override default save method to automatically generate associated images
    # if the original has been changed
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.display_name[:50])
        super(CatalogInfo, self).save(*args, **kwargs)
        self.logo = update_image_field(
            self.logo_original,
            self.logo, 400, 400, 'png')
        self.logo_small = update_image_field(
            self.logo_original,
            self.logo_small, 200, 200, 'png')
        self.ad = update_image_field(
            self.ad_original,
            self.ad, 640, 480, 'jpg')
        super(CatalogInfo, self).save(*args, **kwargs)
