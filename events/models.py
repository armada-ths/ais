from django.db import models
from django.core.urlresolvers import reverse

class Event(models.Model):
    ROLES = (
    ("App", "Applikationsutvecklare"),
    ("AD", "Art Director"),
    ("BD","Backend Developer"),
    ("BE","Bankett: Eventteknikkoordinator"),
    ("BIK","Bankett: Inrednings- och Inkopsgruppledare"),
    ("BL","Bankett: Logistikgruppledare"),
    ("BU","Bankett: Underhallningsgruppledare"),
    ("BH","Banquet Host"),
    ("BRM","Business Relations Manager"),
    ("CM","Campaign Manager"),
    ("CFH","Career Fair Host"),
    ("CFM","Career Fair Manager"),
    ("CW","Copywriter"),
    ("EH","Event Host"),
    ("EM","Event Manager"),
    ("EG","Eventgruppledare"),
    ("FR","Foretagsreception"),
    ("FL","Fotogruppledare"),
    ("FP","Framtida projektledare"),
    ("FU","Frontend-utvecklare"),
    ("GF","Grafisk formgivare"),
    ("HBRE","Head of Business Relations and Events"),
    ("HLCF","Head of Logistics and Career Fair"),
    ("HMCI","Head of Marketing, Communications and Internal Systems"),
    ("H","Host"),
    ("ISM","Internal Systems Manager"),
    ("IWM","IT-Web Manager"),
    ("KF","Kampanj: Filmskapare"),
    ("KO","Kampanjkoordinator"),
    ("LM","Logistics Manager"),
    ("LH","Lounge Host"),
    ("LG","Loungegruppledare"),
    ("MGL","Massgruppledare"),
    ("MAM","Mobile Application Manager"),
    ("P","Photographer"),
    ("PM","Project Manager"),
    ("PGM","Projektgruppsmedlem"),
    ("RM","Recruitment Manager"),
    ("RG","Representationsgruppledare"),
    ("RGL","Representationssittningsgruppledare"),
    ("RGB","Representationssittningsgruppledare Bankett"),
    ("SH","Sambandhelp"),
    ("SH","Service Host"),
    ("SGL","Servicegruppledare"),
    ("SLGL","Specialstyrkan: Logistikgruppledare"),
    ("STGL","Specialstyrkan: Teknikgruppledare"),
    ("SK","Sponskoordinator"),
    ("SSM","Sponsorship and Service Manager"),
    ("SU","Systemutvecklare"),
    ("TF","Task force"),
    ("TL","Team Leader"),
    ("URH","University Relations Host"),
    )

    name = models.CharField(max_length=75)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    capacity = models.IntegerField(default=1, blank=True, null=True)
    needs_approval = models.BooleanField()
    description = models.TextField(blank=True)
    registration_open = models.DateTimeField()
    registration_last_day = models.DateTimeField()
    registration_last_day_cancel = models.DateTimeField()
    roles = models.CharField(max_length=3, choices=ROLES)
    make_event_public = models.BooleanField()

    def __unicode__(self):
        return self.name

def get_absolute_url(self):
    return reverse('event_edit', kwargs={'pk': self.pk})

class EventAttendence(models.Model):
    STATUS = (
    ("A","Approved"),
    ("C","Canceled"),
    ("D","Declined"),
    ("S","Submitted"),
    )

    person = models.CharField(max_length=75)
    status = models.CharField(max_length=3, choices=STATUS)
    name = models.CharField(max_length=75)
    mobile = models.IntegerField(default=1, blank=True, null=True)
    allergies = models.CharField(max_length=75)
    attending = models.BooleanField()

    def __unicode__(self):
        return self.name
