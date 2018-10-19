from django.db import models
from lib.image import UploadToDirUUID
from django.contrib.auth.models import User
from django.contrib.gis.db import models

from accounting.models import Order
from banquet.models import Banquet, Participant
from recruitment.models import RecruitmentApplication
from fair.models import Fair
from people.models import DietaryRestriction


class CatalogueIndustry(models.Model):
	industry = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.industry
	class Meta: default_permissions = []


class CatalogueValue(models.Model):
	value = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.value
	class Meta: default_permissions = []


class CatalogueEmployment(models.Model):
	employment = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.employment
	class Meta: default_permissions = []


class CatalogueLocation(models.Model):
	location = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.location
	class Meta: default_permissions = []


class CatalogueBenefit(models.Model):
	benefit = models.CharField(blank = False, max_length = 255)
	def __str__(self): return self.benefit
	class Meta: default_permissions = []


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
	company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
	fair = models.ForeignKey('fair.Fair', on_delete=models.CASCADE)
	contact_persons = models.ManyToManyField(User, blank = True)
	contact = models.ForeignKey('companies.CompanyContact', null=True, blank=True, on_delete=models.CASCADE)
	booth_height = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Height of the booth (cm)')
	electricity_total_power = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Estimated power consumption (W)')
	electricity_socket_count = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Number of sockets')
	electricity_equipment = models.TextField(blank = True, null = True, verbose_name = 'Description of equipment')
	catalogue_about = models.TextField(blank = True, null = True, max_length = 600)
	catalogue_purpose = models.TextField(blank = True, null = True, max_length = 600)
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
	
	transport_statuses = [
		('NOT_BOOKED', 'Not booked'),
		('BOOKED', 'Booked'),
		('ARKAD', 'Transported by Arkad'),
		('NOT_APPLICABLE', 'Not applicable'),
		('EXCEPTION', 'Exception'),
		('IN_CONTACT', 'In contact')
	]
	
	transport_to = models.CharField(choices = transport_statuses, null = False, blank = False, default = 'NOT_BOOKED', max_length = 30)
	transport_from = models.CharField(choices = transport_statuses, null = False, blank = False, default = 'NOT_BOOKED', max_length = 30)
	transport_comment = models.TextField(blank = True, null = True)
	
	@property
	def count_lunch_tickets(self):
		count_ordered = 0
		
		for order in Order.objects.filter(purchasing_company = self.company, product = self.fair.product_lunch_ticket):
			count_ordered += order.quantity
		
		count_created = LunchTicket.objects.filter(exhibitor = self).count()
		
		return {
			'ordered': count_ordered,
			'created': count_created
		}
	
	@property
	def count_banquet_tickets(self):
		count_ordered = 0
		count_created = 0
		
		for banquet in Banquet.objects.filter(fair = self.fair):
			if banquet.product is not None:
				for order in Order.objects.filter(purchasing_company = self.company, product = banquet.product):
					count_ordered += order.quantity
			
			count_created += Participant.objects.filter(banquet = banquet, company = self.company).count()
		
		return {
			'ordered': count_ordered,
			'created': count_created
		}
	
	def __str__(self): return '%s at %s' % (self.company.name, self.fair.name)
	
	class Meta:
		default_permissions = []
		permissions = [
			('base', 'View the Exhibitors tab'),
			('view_all', 'Always view all exhibitors'),
			('create', 'Create new exhibitors'),
			('modify_contact_persons', 'Modify contact persons'),
			('modify_transport', 'Modify transport details')
		]


class LunchTicketDay(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(blank = False, null = False, max_length = 255)
	
	class Meta:
		default_permissions = []
		ordering = ['fair', 'name']
	
	def __str__(self): return self.name + ' at ' + self.fair.name


class LunchTicket(models.Model):
	email_address = models.EmailField(blank = False, null = False, max_length = 255, verbose_name = 'E-mail address')
	comment = models.CharField(blank = True, null = True, max_length = 255)
	exhibitor = models.ForeignKey(Exhibitor, on_delete = models.CASCADE)
	day = models.ForeignKey(LunchTicketDay, on_delete = models.CASCADE)
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True)
	
	class Meta:
		default_permissions = []
		ordering = ['pk']


class LunchTicketScan(models.Model):
	lunch_ticket = models.ForeignKey(LunchTicket, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add = True, blank = False, null = False)
	
	class Meta:
		default_permissions = []


class ExhibitorView(models.Model):
	'''
	A special model that houses information which fields a certain user wants to see in /fairs/%YEAR/exhibitors view
	'''
	selectable_fields = {
		'contact_persons': 'Contact persons',
		'transport_to': 'Transport to the fair',
		'transport_from': 'Transport from the fair',
		'transport_comment': 'Transport comment',
		'placement_wish': 'Placement wish',
		'placement_comment': 'Placement comment',
		'electricity_total_power': 'Total power (W)',
		'electricity_socket_count': 'Socket count',
		'electricity_equipment': 'Electricity equipment',
		'booth_height': 'Booth height (cm)',
		'count_lunch_tickets': 'Lunch tickets',
		'count_banquet_tickets': 'Banquet tickets'
	}
	
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	choices = models.TextField()

	def create(self):
		self.choices = 'contact_persons transport_from transport_to count_lunch_tickets count_banquet_tickets'
		self.save()
		
		return self
	
	class Meta:
		default_permissions = []


class Location(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	parent = models.ForeignKey('exhibitors.Location', on_delete = models.CASCADE, null = True, blank = True)
	name = models.CharField(blank = False, null = False, max_length = 255)
	background = models.ImageField(upload_to = UploadToDirUUID('locations'), null = True, blank = True)
	
	class Meta:
		ordering = ['fair', 'name']
		unique_together = [['fair', 'name']]
	
	def __str__(self): return self.name


class Booth(models.Model):
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	name = models.CharField(blank = False, null = False, max_length = 255)
	boundaries = models.PolygonField(blank = True, null = True)
	
	class Meta:
		ordering = ['location', 'name']
		unique_together = [['location', 'name']]
	
	def __str__(self): return str(self.location) + ' -> ' + self.name


class ExhibitorInBooth(models.Model):
	exhibitor = models.ForeignKey(Exhibitor, on_delete = models.CASCADE)
	booth = models.ForeignKey(Booth, on_delete = models.CASCADE)
	comment = models.CharField(max_length = 255, null = True, blank = True)
	
	class Meta:
		ordering = ['exhibitor', 'booth']
		unique_together = [['exhibitor', 'booth']]
	
	def __str__(self): return self.exhibitor + ' in ' + self.booth
