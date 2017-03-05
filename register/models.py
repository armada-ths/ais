from django.db import models
from django.db.models import DEFERRED


# A 'Contact' is a person working for a 'Company'
class SignupContract(models.Model):
    name = models.CharField(max_length=30)
    contract = models.FileField(upload_to='contracts/%Y%m%d/')
    fair = models.ForeignKey('fair.Fair')
    current = models.BooleanField(default=False);

    _loaded_values = None

    ## These special overrides are meant to prevent anyone from changing an uploaded contract
    ## that some companies might already have agreed to
    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        if self._loaded_values:
            if self.contract != self._loaded_values['contract'] or self.fair.id != self._loaded_values['fair_id']:
                #Contarct changed! Not allowed!
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
    contract = models.ForeignKey('SignupContract')
    timestamp = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey('companies.Contact')
    
    def __str__(self):
        return self.contact.name + " at " + self.contact.belongs_to.name
