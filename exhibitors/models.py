from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, update_image_field
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from recruitment.models import RecruitmentApplication
from fair.models import Fair
from transportation.models import TransportationOrder

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Job type that an exhibitor offers
class JobType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class TransportationAlternative(models.Model):
    name = models.CharField(max_length=150)
    types = [
            ('3rd_party', 'Third party'),
            ('self', 'By Customer'),
            ('internal', 'Fair arranger')
            ]
    transportation_type = models.CharField(choices=types, null=True, blank=True, max_length=30)
    inbound = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CatalogueIndustry(models.Model):
	industry = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.industry


class CatalogueValue(models.Model):
	value = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.value


class CatalogueEmployment(models.Model):
	employment = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.employment


class CatalogueLocation(models.Model):
	location = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.location


class CatalogueBenefit(models.Model):
	benefit = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.benefit


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
	company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
	fair = models.ForeignKey('fair.Fair', on_delete=models.CASCADE)
	hosts = models.ManyToManyField(User, blank=True)
	contact = models.ForeignKey('companies.CompanyContact', null=True, blank=True, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
	booth_number = models.IntegerField(blank=True, null=True)
	fair_location = models.OneToOneField('locations.Location', blank=True, null=True, on_delete=models.CASCADE)
	about_text = models.TextField(blank=True)
	facts_text = models.TextField(blank=True)
	accept_terms = models.BooleanField(default=False)
	booth_height = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Height of the booth (cm)')
	electricity_total_power = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Estimated power consumption (W)')
	electricity_socket_count = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Number of sockets')
	electricity_equipment = models.TextField(blank = True, null = True, verbose_name = 'Description of equipment')
	catalogue_about = models.TextField(blank = True, null = True)
	catalogue_purpose = models.TextField(blank = True, null = True)
	catalogue_logo_squared = models.ImageField(upload_to = UploadToDirUUID('exhibitors', 'catalogue_logo_squared'), blank = True)
	catalogue_logo_freesize = models.ImageField(upload_to = UploadToDirUUID('exhibitors', 'catalogue_logo_freesize'), blank = True)
	catalogue_contact_name = models.CharField(blank = True, null = True, max_length = 255, verbose_name = 'Contact person\'s name')
	catalogue_contact_email_address = models.CharField(blank = True, null = True, max_length = 255, verbose_name = 'Contact person\'s e-mail address')
	catalogue_contact_phone_number = models.CharField(blank = True, null = True, max_length = 255, verbose_name = 'Contact person\'s phone number')
	catalogue_industries = models.ManyToManyField(CatalogueIndustry, blank = True)
	catalogue_values = models.ManyToManyField(CatalogueValue, blank = True)
	catalogue_employments = models.ManyToManyField(CatalogueEmployment, blank = True)
	catalogue_locations = models.ManyToManyField(CatalogueLocation, blank = True)
	catalogue_benefits = models.ManyToManyField(CatalogueBenefit, blank = True)
	catalogue_average_age = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Average age of employees')
	catalogue_founded = models.PositiveIntegerField(blank = True, null = True)
	
	placement_wishes = [
		('MIXED', 'Mixed with companies from other industries'),
		('SIMILAR', 'Next to similar companies'),
	]
	
	placement_wish = models.CharField(choices = placement_wishes, blank = True, null = True, max_length = 255)
	placement_comment = models.TextField(blank = True, null = True, verbose_name = 'Additional wishes regarding placement at the fair')
	
	# For the logistics team
	comment = models.TextField(blank=True)
	
	statuses = [
		('accepted', 'Accepted'),
		('registered', 'Registered'),
		('complete_registration', 'Completed Registration'),
		('complete_registration_submit', 'CR - Submitted'),
		('complete_registration_start', 'CR - In Progress'),
		('complete_registration_terms', 'CR - Accepted Terms'),
		('contacted_by_host', 'Contacted by host'),
		('confirmed', 'Confirmed'),
		('checked_in', 'Checked in'),
		('checked_out', 'Checked out'),
		('withdrawn', 'Withdrawn'),
	]
	
	status = models.CharField(choices=statuses, null=True, blank=True, max_length=30)
	logo = models.ImageField(upload_to=UploadToDirUUID('exhibitors', 'logo_original'), blank=True)
	location_at_fair = models.ImageField(upload_to=UploadToDirUUID('exhibitors', 'location_at_fair'), blank=True)
	
	inbound_transportation = models.ForeignKey(TransportationAlternative, on_delete=models.SET_NULL, null=True, blank=True, related_name='inbound_transportation', verbose_name='Transportation to the fair')
	outbound_transportation = models.ForeignKey(TransportationAlternative, on_delete=models.SET_NULL, null=True, blank=True, related_name='outbound_transportation', verbose_name='Transportation from the fair')
	pickup_order = models.ForeignKey(TransportationOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='pickup_order')
	delivery_order = models.ForeignKey(TransportationOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_order')
	
	tags = models.ManyToManyField('fair.Tag', blank=True)
	
	job_types = models.ManyToManyField(JobType, blank=True)
	
	def total_cost(self):
		return sum([order.price() for order in self.order_set.all()])
	
	def superiors(self):
		accepted_applications = [RecruitmentApplication.objects.filter(status='accepted', user=host).first() for host in
									self.hosts.all()]
		return [application.superior_user for application in accepted_applications if application and application.superior_user]
	
	def __str__(self):
		return '%s at %s' % (self.company.name, self.fair.name)
	
	class Meta:
		permissions = (('base', 'Exhibitors'),)


class ExhibitorView(models.Model):
    '''
    A special model that houses information which fields a certain user wants to see in /fairs/%YEAR/exhibitors view
    '''
    # A set of field names from Exhibitor model, that are not supposed to be selectable
    ignore = {'user', 'id', 'pk', 'logo'}
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The idea is to store field name for fields that a user selected to view (shouldn't be too many)
    # and make this procedural, so if the Exhibitor model changes, no large changes to this model would be necessary
    choices = models.TextField()

    def create(self):
        # A set of field names from Exhibitor model, that are shown by default
        default = {'location', 'hosts', 'status'}

        for field in default:
            self.choices = self.choices + ' ' + field
        self.save()
        return self

# Work field that an exhibitor operates in
class WorkField(models.Model):
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
        WorkField, blank=True, null=True, related_name='+', on_delete=models.CASCADE)
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
