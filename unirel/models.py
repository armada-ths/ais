import uuid

from django.db import models

from fair.models import Fair
from companies.models import Company
from people.models import DietaryRestriction

class Participant(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, blank = False, null = False, on_delete = models.CASCADE, related_name = 'unirel_participant_company', verbose_name = 'Organization')
	token = models.CharField(max_length = 255, null = False, blank = False, default = uuid.uuid4, unique = True)
	name = models.CharField(max_length = 75, blank = False, null = False)
	email_address = models.EmailField(max_length = 75, blank = False, null = False, verbose_name = 'E-mail address')
	phone_number = models.CharField(max_length = 75, blank = True, null = True)
	addon_banquet = models.BooleanField(choices = [(True, 'Yes'), (False, 'No')], default = False)
	addon_sleep = models.BooleanField(choices = [(True, 'Yes'), (False, 'No')], default = False)
	addon_lunch = models.BooleanField(choices = [(True, 'Yes'), (False, 'No')], default = False)
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True, related_name = 'unirel_participant_dietaryrestrictions')
	
	def __str__(self): return self.name
	
	class Meta:
		ordering = ['fair', 'company', 'name']
		permissions = [('base', 'University relations')]
