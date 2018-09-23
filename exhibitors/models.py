from django.db import models
from lib.image import UploadToDirUUID
from django.contrib.auth.models import User

from recruitment.models import RecruitmentApplication
from fair.models import Fair
from people.models import DietaryRestriction


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
	hosts = models.ManyToManyField(User, blank = True)
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
	
	# For the logistics team
	comment = models.TextField(blank=True)
	
	logo = models.ImageField(upload_to=UploadToDirUUID('exhibitors', 'logo_original'), blank=True)
	location_at_fair = models.ImageField(upload_to=UploadToDirUUID('exhibitors', 'location_at_fair'), blank=True)
	
	transport_statuses = [
		('NOT_BOOKED', 'Not booked'),
		('BOOKED', 'Booked'),
		('NOT_APPLICABLE', 'Not applicable')
	]
	
	transport_to = models.CharField(choices = transport_statuses, null = False, blank = False, default = 'NOT_BOOKED', max_length = 30)
	transport_from = models.CharField(choices = transport_statuses, null = False, blank = False, default = 'NOT_BOOKED', max_length = 30)
	transport_comment = models.TextField(blank = True, null = True)
	
	def superiors(self):
		accepted_applications = [RecruitmentApplication.objects.filter(status='accepted', user=host).first() for host in self.hosts.all()]
		return [application.superior_user for application in accepted_applications if application and application.superior_user]
	
	def __str__(self):
		return '%s at %s' % (self.company.name, self.fair.name)
	
	class Meta:
		permissions = [
			('base', 'Exhibitors'),
			('transport', 'Modify exhibitor transport details')
		]


class LunchTicketDay(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(blank = False, null = False, max_length = 255)
	
	class Meta:
		ordering = ['fair', 'name']
	
	def __str__(self): return self.name + ' at ' + self.fair.name


class LunchTicket(models.Model):
	email_address = models.EmailField(blank = False, null = False, max_length = 255, verbose_name = 'E-mail address')
	comment = models.CharField(blank = True, null = True, max_length = 255)
	exhibitor = models.ForeignKey(Exhibitor, on_delete = models.CASCADE)
	day = models.ForeignKey(LunchTicketDay, on_delete = models.CASCADE)
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True)
	
	class Meta:
		ordering = ['pk']


class LunchTicketScan(models.Model):
	lunch_ticket = models.ForeignKey(LunchTicket, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add = True, blank = False, null = False)


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
        default = {'hosts'}

        for field in default:
            self.choices = self.choices + ' ' + field
        self.save()
        return self
