from datetime import date
from lib.image import UploadToDirUUID

from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from people.models import DietaryRestriction

def get_common_name(self):
	return '%s %s' % (self.first_name, self.last_name) if self.first_name and self.last_name else self.username

User.add_to_class("__str__", get_common_name)

def current_fair():
	try: return Fair.objects.get(current = True).id
	except Exception: return None


def default_name(): 
    return "Armada %d"%(date.today().year)


def get_random_32_length_string():
    return get_random_string(32)


class Fair(models.Model):
	name = models.CharField(max_length = 100, default = default_name)
	year = models.IntegerField(default = date.today().year)
	description = models.TextField(max_length = 500, default = default_name)

	registration_start_date = models.DateTimeField(null = True)
	registration_end_date = models.DateTimeField(null = True)
	complete_registration_start_date = models.DateTimeField(null = True, blank = True)
	complete_registration_close_date = models.DateTimeField(null = True, blank = True)

	current = models.BooleanField(default = False)

	product_lunch_ticket = models.ForeignKey('accounting.Product', blank = True, null = True)

	def is_member_of_fair(self, user):
		if user.is_superuser: return True
	
		for recruitment_period in self.recruitmentperiod_set.all():
			if recruitment_period.recruitmentapplication_set.filter(user=user, status='accepted').exists():
				return True
		
		return False

	def save(self, *args, **kwargs):
		if self.current:
			for fair in Fair.objects.filter(current=True):
				fair.current = False
				fair.save()
			self.current = True
		super(Fair, self).save(*args, **kwargs)

	def __str__(self): return self.name


class FairDay(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	date = models.DateField(blank = False, null = False, max_length = 255)
	
	class Meta:
		default_permissions = []
		ordering = ['fair', 'date']
	
	def __str__(self): return str(self.date)


class OrganizationGroup(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(max_length = 255)
	
	def __str__(self): return self.name
	
	class Meta:
		ordering = ['fair', 'name']


class Partner(models.Model):
	name = models.CharField(max_length=50)
	fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to=UploadToDirUUID('partners', 'logo'))
	url = models.CharField(max_length=300)
	main_partner = models.BooleanField()

	def __str__(self): return self.name


class Tag(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=500)

	def __str__(self): return self.name


class LunchTicketTime(models.Model):
	day = models.ForeignKey(FairDay, on_delete = models.CASCADE)
	name = models.CharField(blank = False, null = False, max_length = 255)
	
	class Meta:
		default_permissions = []
		ordering = ['day', 'name']
	
	def __str__(self): return str(self.day) + ' ' + self.name


class LunchTicket(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	token = models.CharField(max_length = 255, null = False, blank = False, default = get_random_32_length_string, unique = True)
	used = models.BooleanField(default = False, blank = False, null = False)
	email_address = models.EmailField(blank = True, null = True, max_length = 255, verbose_name = 'E-mail address')
	comment = models.CharField(blank = True, null = True, max_length = 255)
	company = models.ForeignKey('companies.Company', on_delete = models.CASCADE, blank = True, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
	day = models.ForeignKey(FairDay, on_delete = models.CASCADE)
	time = models.ForeignKey(LunchTicketTime, on_delete = models.SET_NULL, blank = True, null = True)
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True)
	
	class Meta:
		permissions = [('lunchtickets', 'Manage lunch tickets')]
		default_permissions = []
		ordering = ['pk']


class LunchTicketScan(models.Model):
	lunch_ticket = models.ForeignKey(LunchTicket, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add = True, blank = False, null = False)
	
	class Meta:
		default_permissions = []
