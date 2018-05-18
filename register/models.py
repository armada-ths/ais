from django.db import models
from django.db.models import DEFERRED
from django.utils import timezone

# A 'Contact' is a person working for a 'Company'
class SignupContract(models.Model):
	name = models.CharField(max_length = 30)
	contract = models.FileField(upload_to = 'contracts/%Y%m%d/')
	fair = models.ForeignKey('fair.Fair', on_delete = models.CASCADE)
	current = models.BooleanField(default = False);

	_loaded_values = None

	# These special overrides are meant to prevent anyone from changing an uploaded contract that some companies might already have agreed to
	@classmethod
	def from_db(cls, db, field_names, values):
		instance = super().from_db(db, field_names, values)
		instance._loaded_values = dict(zip(field_names, values))
		
		return instance

	def save(self, *args, **kwargs):
		if self._loaded_values:
			if self.contract != self._loaded_values['contract'] or self.fair.id != self._loaded_values['fair_id']:
				raise ValueError('Not allowed to change contract, upload a new one instead!')
		
		if self.current:
			# set all other for this fair to false to guarantee only one is current
			for contract in SignupContract.objects.filter(fair=self.fair, current=True):
				contract.current = False
				contract.save()
			
			self.current = True
		
		super(SignupContract, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class SignupLog(models.Model):
	contract = models.ForeignKey('SignupContract', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	company = models.ForeignKey('companies.Company', null= True, on_delete=models.CASCADE, related_name = "signature")
	company_contact = models.ForeignKey('companies.CompanyContact', on_delete = models.CASCADE, null = True, blank = True)
    
	types = [
		('initial', 'Initial'),
		('complete', 'Complete'),
	]

	type = models.CharField(choices=types, null=True, blank=True, max_length=30)

	def __str__(self):
		return self.company_contact.company.name + " for " + self.contract.name
	
	class Meta:
		ordering = ["-timestamp",]
