from django.db import models
from django.contrib.auth.models import User

from companies.models import Company
from accounting.models import Product
from fair.models import Fair


class Banquet(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	date = models.DateTimeField()
	location = models.CharField(max_length = 75, blank = True, null = True)
	product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Product to link the banquet with')


class DietaryPreference(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	preference = models.CharField(max_length = 75, blank = False, null = False)


class Participant(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, blank = True, null = True, on_delete = models.CASCADE)
	user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = True, null = True)          # None if a user is provided, required for others
	email_address = models.CharField(max_length = 75, blank = True, null = True) # None if a user is provided, required for others
	phone_number = models.CharField(max_length = 75, blank = True, null = True)  # None if a user is provided, required for others
	dietary_preferences = models.ManyToManyField(DietaryPreference)


class Invitation(models.Model):
	token = models.CharField(max_length = 128, unique = True, blank = False, null = False)
	participant = models.ForeignKey(Participant, blank = True, null = True, on_delete = models.CASCADE) # filled in when the participant has been created from this invitation
	name = models.CharField(max_length = 75, blank = True, null = True)
	email_address = models.CharField(max_length = 75, blank = True, null = True)
	reason = models.CharField(max_length = 75, blank = True, null = True)
	price = models.PositiveIntegerField() # can be zero
