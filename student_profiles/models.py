from django.db import models
from django.utils import timezone
from django.utils.timezone import utc

import uuid

class StudentProfile(models.Model):
    '''
    A striped down version of a user profile
    Is used by api and banquet apps

    Note:   that nickname is used in tests.py for both this app and matching, if
            this is changed here, these tests will fail on setUp.
    '''
    nickname = models.CharField(max_length=512, blank=True, default='Student')
    id_string = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    # optional fields
    linkedin_profile = models.CharField(max_length=128, null=True, blank=True)
    facebook_profile = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    #this is used for debugging purposes of the classifier, should be removed later
    classifier_log  = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nickname


class MatchingResult(models.Model):
    '''
    Results from the matching algorithm
    Is used by the matching algorithm to put data and for
    the app and web to display the data.

    Necessary field(s):
        student (fk)    - foreign key to StudentProfile
        exhibitor (fk)  - foreign key to an Exhibitor
        fair (fk)       - foregin key to which fair
        score (int)     - integer value repr. how good the matching is

    '''
    student     = models.ForeignKey(StudentProfile)
    exhibitor     = models.ForeignKey('exhibitors.Exhibitor', null=True)
    fair        = models.ForeignKey('fair.Fair')
    score       = models.PositiveIntegerField(default=0)
    created     = models.DateTimeField(editable=False, null=True, blank=True)
    updated     = models.DateTimeField(null=True, blank=True)
    class Meta:
        default_permissions = ()
        verbose_name = 'results matching'

    def save(self, *args, **kwargs):
        ''' Used only to update timestamp '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(MatchingResult, self).save(*args, **kwargs)

    def __str__(self):
        return '%s score for %s\t = %i'%(self.student.nickname, self.exhibitor.company.name, self.score)
