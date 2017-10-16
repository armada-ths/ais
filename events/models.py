from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.conf import settings
from lib.image import UploadToDirUUID, UploadToDir, update_image_field
import os
from fair.models import Fair, Tag
from recruitment.models import ExtraField
from django.utils import timezone


# An 'Event' belongs to a specific 'Fair'
class Event(models.Model):
    # Add event attendence per model
    fair = models.ForeignKey(Fair)
    name = models.CharField(max_length=75)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    capacity = models.PositiveSmallIntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    description_short = models.TextField(blank=True)
    location = models.CharField(max_length=75, blank=True)
    attendence_description = models.TextField(
        blank=True,
        help_text="This is a text only shown in the attendence form, example \
        'To be accepted to this event you need to pay the event fee of \
        500 SEK'")
    attendence_approvement_required = models.BooleanField(
        default=True,
        help_text="If this is checked all users that attends the event needs to \
        be accepted by an admin.")
    external_signup_url = models.URLField(blank=True)
    registration_required = models.BooleanField(default=True)
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    registration_last_day_cancel = models.DateTimeField(
        null=True,
        help_text="Last day a user can cancel the attendence to the event")
    public_registration = models.BooleanField(
        default=False,
        help_text="If users without an account should be able to sign up for \
        this event.")
    published = models.BooleanField(
        default=False,
        help_text="If the event should be published in the apps and on the website."
    )
    allowed_groups = models.ManyToManyField(
        Group, blank=True,
        help_text="Choose which groups in armada should be able to see and \
        attend this event. NOTE: No groups make the event accesible to all \
        ais-users.")
    send_submission_mail = models.BooleanField(
        default=False,
        help_text="If checked an email will be sent when a user attends \
        the event")
    submission_mail_subject = models.CharField(max_length=78, blank=True)
    submission_mail_body = models.TextField(blank=True)

    confirmation_mail_subject = models.CharField(max_length=78, blank=True)
    confirmation_mail_body = models.TextField(blank=True)

    rejection_mail_subject = models.CharField(max_length=78, blank=True)
    rejection_mail_body = models.TextField(blank=True)

    image_original = models.ImageField(
            upload_to=UploadToDirUUID('events', 'image_original'), blank=True)
    image = models.ImageField(
            upload_to=UploadToDir('events', 'image'), blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    extra_field = models.ForeignKey(ExtraField, blank=True, null=True)

    def __str__(self):
        return '%s: %s'%(self.fair, self.name)

    def save(self, *args, **kwargs):
        if not self.extra_field:
            self.extra_field = ExtraField.objects.create()
# TODO: figure out the way to pass the actual name that will be used, not the file's original one!!!
#        self.image = update_image_field(
#            self.image_original,
#            self.image, 1000, 1000, 'jpg')
        super(Event, self).save(*args, **kwargs)

# An EventQuestion belongs to a specific Event
class EventQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.TextField(blank=False)
    required = models.BooleanField(default=False)

    def __str__(self):
        return '%s'%(self.question_text)

# An EventAttendence is for a specific User to attend a specific Event
class EventAttendence(models.Model):
    STATUS = (
    ("A","Approved"),
    ("C","Canceled"),
    ("D","Declined"),
    ("S","Submitted"),
    )

    user = models.ForeignKey(User, null=True, default=None, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default="S")
    submission_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        if self.user is not None:
            user = self.user.get_full_name()
        else:
            user = "External user"
        return '%s - %s - %s' % (self.event.name, user, self.get_status_display())


# An EventAnswer is the answer to a specific EventQuestion for a specific User
class EventAnswer(models.Model):
    question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE)
    attendence = models.ForeignKey(EventAttendence, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)

    def __str__(self):
        return '%s'%(self.question.question_text)
