from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, update_image_field
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from recruitment.models import RecruitmentApplication


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
    fair_location = models.OneToOneField('locations.Location', blank=True, null=True)
    estimated_arrival_of_representatives = models.DateTimeField(null=True, blank=True)

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

    # Invoice
    invoice_reference = models.CharField(max_length=200, blank=True)
    invoice_reference_phone_number = models.CharField(max_length=200, blank=True)
    invoice_organisation_name = models.CharField(max_length=200, blank=True)
    invoice_address = models.CharField(max_length=200, blank=True)
    invoice_address_po_box = models.CharField(max_length=200, blank=True)
    invoice_address_zip_code = models.CharField(max_length=100, blank=True)
    invoice_identification = models.CharField(max_length=200, blank=True)
    invoice_additional_information = models.CharField(max_length=500, blank=True)

    # Transport to fair
    transport_to_fair_types = [
        ('external_transport', 'Yes, with an external delivery firm'),
        ('arkad_transport', 'Yes, with transport from Arkad in Lund'),
        ('self_transport', 'No, we will bring our goods ourselves'),
    ]

    transport_to_fair_type = models.CharField(choices=transport_to_fair_types, null=True, blank=True, max_length=30)
    number_of_packages_to_fair = models.IntegerField(default=0)
    number_of_pallets_to_fair = models.IntegerField(default=0)
    estimated_arrival = models.DateTimeField(null=True, blank=True)

    # Transport from fair
    transport_from_fair_types = [
        ('third_party_builders_transport',
         'We use a third-party to build our stand who will transport our goods from the fair'),
        ('armada_transport', 'We use Armada Transport'),
        ('self_transport',
         'We will arrange our own transportation immediately after the fair (note that there is limited access for larger transportation services as the fair closes and it may take some time before your equipment can be picked up)'),
    ]

    transport_from_fair_type = models.CharField(choices=transport_from_fair_types, null=True, blank=True,
                                                max_length=300)
    number_of_packages_from_fair = models.IntegerField(default=0)
    number_of_pallets_from_fair = models.IntegerField(default=0)

    transport_from_fair_address = models.CharField(max_length=200, blank=True)
    transport_from_fair_zip_code = models.CharField(max_length=100, blank=True)
    transport_from_fair_recipient_name = models.CharField(max_length=200, blank=True)
    transport_from_fair_recipient_phone_number = models.CharField(max_length=200, blank=True)

    # Marketing
    wants_information_about_events = models.BooleanField(default=False)
    wants_information_about_targeted_marketing = models.BooleanField(default=False)
    wants_information_about_osqledaren = models.BooleanField(default=False)

    def total_cost(self):
        return sum([order.price() for order in self.order_set.all()])

    def superiors(self):
        accepted_applications = [RecruitmentApplication.objects.filter(status='accepted', user=host).first() for host in
                                 self.hosts.all()]
        return [application.superior_user for application in accepted_applications if application.superior_user]

    def __str__(self):
        return '%s at %s' % (self.company.name, self.fair.name)


    class Meta:
        permissions = (('view_exhibitors', 'View exhibitors'),)


class BanquetteAttendant(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)  # Null for exhibitor representants
    exhibitor = models.ForeignKey(Exhibitor, null=True, blank=True)  # Null for non-exhibitor representants
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    linkedin_url = models.URLField(blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    genders = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(choices=genders, max_length=10)
    phone_number = models.CharField(max_length=200)
    allergies = models.CharField(max_length=1000, blank=True)
    student_ticket = models.BooleanField(default=False)
    wants_alcohol = models.BooleanField(default=True)
    wants_lactose_free_food = models.BooleanField(default=False)
    wants_gluten_free_food = models.BooleanField(default=False)
    wants_vegetarian_food = models.BooleanField(default=True)

    table_name = models.CharField(max_length=20, null=True, blank=True)
    seat_number = models.SmallIntegerField(null=True, blank=True)
    ignore_from_placement = models.BooleanField(default=False)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.exhibitor)


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
    short_description = models.CharField(max_length=200, blank=True)
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

    location_at_fair_original = models.ImageField(
        upload_to=UploadToDirUUID('exhibitors', 'location_at_fair_original'),
        blank=True
    )

    location_at_fair = models.ImageField(
        upload_to=UploadToDir('exhibitors', 'location_at_fair'),
        blank=True
    )

    # ManyToMany relationships
    programs = models.ManyToManyField('people.Programme', blank=True)
    main_work_field = models.ForeignKey(
        WorkField, blank=True, null=True, related_name='+')
    work_fields = models.ManyToManyField(
        WorkField, blank=True, related_name='+')
    job_types = models.ManyToManyField(JobType, blank=True)
    continents = models.ManyToManyField(Continent, blank=True)
    values = models.ManyToManyField(Value, blank=True)
    tags = models.ManyToManyField('fair.Tag', blank=True)

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
        self.location_at_fair = update_image_field(
            self.location_at_fair_original,
            self.location_at_fair, 1000, 1000, 'png')
        super(CatalogInfo, self).save(*args, **kwargs)
