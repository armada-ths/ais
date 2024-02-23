import uuid

from django.conf import settings
from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, update_image_field


class Language(models.Model):
    name = models.CharField(max_length=100)
    short = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Programme(models.Model):
    name = models.CharField(max_length=100)
    shortening = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DietaryRestriction(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDERS = (("male", "Male"), ("female", "Female"), ("other", "Other"))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, default=-1, primary_key=True, on_delete=models.CASCADE
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)
    other_dietary_restrictions = models.CharField(max_length=75, blank=True, null=True)
    no_dietary_restrictions = models.BooleanField(default=False)
    programme = models.ForeignKey(
        Programme,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Program",
    )
    registration_year = models.IntegerField(null=True, blank=True)
    planned_graduation = models.IntegerField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True, verbose_name="Linkedin URL")
    armada_email = models.EmailField(null=True, blank=True, verbose_name="Armada Email")
    token = models.CharField(max_length=255, null=True, blank=False, default=uuid.uuid4)
    slack_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Slack ID"
    )
    preferred_language = models.ForeignKey(
        Language, null=True, blank=True, on_delete=models.CASCADE
    )
    kth_synchronize = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name="Synchronize account data with KTH",
    )

    picture_original = models.ImageField(
        upload_to=UploadToDirUUID("profiles", "picture_original"), blank=True
    )
    picture = models.ImageField(
        upload_to=UploadToDir("profiles", "picture"), blank=True
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        db_table = "profile"
        permissions = [("base", "People")]
