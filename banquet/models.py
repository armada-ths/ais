import uuid
from django.db import models
from django.contrib.auth.models import User

from companies.models import Company
from people.models import DietaryRestriction
from accounting.models import Product
from fair.models import Fair


class Banquet(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	date = models.DateTimeField()
	location = models.CharField(max_length = 75, blank = True, null = True)
	product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Product to link the banquet with')

	def __str__(self): return self.name

# For alcohol
BOOL_CHOICES = [(True, 'Yes'), (False, 'No')]


class Participant(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, blank = True, null = True, on_delete = models.CASCADE)
	user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = True, null = True)	     # None if a user is provided, required for others
	email_address = models.EmailField(max_length = 75, blank = True, null = True, verbose_name = 'E-mail address') # None if a user is provided, required for others
	phone_number = models.CharField(max_length = 75, blank = True, null = True)  # None if a user is provided, required for others
	dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank = True)
	alcohol = models.BooleanField(choices = BOOL_CHOICES, default = True)

	def __str__(self): return (self.company.name + ' : ' + self.name) if self.company else self.name


class Invitation(models.Model):
	banquet = models.ForeignKey(Banquet, on_delete = models.CASCADE)
	token = models.CharField(max_length = 255, null = True, blank = False, default = uuid.uuid4, unique = True)
	user = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE, related_name = 'banquet_invitation_user')
	participant = models.ForeignKey(Participant, blank = True, null = True, on_delete = models.CASCADE) # filled in when the participant has been created from this invitation
	name = models.CharField(max_length = 75, blank = True, null = True)
	email_address = models.CharField(max_length = 75, blank = True, null = True)
	reason = models.CharField(max_length = 75, blank = True, null = True)
	price = models.PositiveIntegerField() # can be zero
	denied = models.BooleanField(default=False)

	@classmethod
	def create(cls, banquet, participant, name, email_address, reason, price, user):
		return cls(
			banquet=banquet,
			participant=participant,
			name=name,
			email_address=email_address,
			reason=reason,
			price=price,
			user=user,
		)

	def __str__(self): return (self.name)
