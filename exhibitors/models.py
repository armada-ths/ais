from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, \
    format_png, format_jpg, should_generate
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os


MEDIA_ROOT = settings.MEDIA_ROOT


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
    company = models.ForeignKey('companies.Company')
    fair = models.ForeignKey('fair.Fair')
    hosts = models.ManyToManyField(User, blank=True)
    contact = models.ForeignKey('companies.Contact', null=True, blank=True)

    invoice_identification = models.CharField(max_length=64, blank=True)
    invoice_address = models.CharField(max_length=64, blank=True)
    invoice_address_zip_code = models.CharField(max_length=8, blank=True)
    invoice_address_city = models.CharField(max_length=32, blank=True)
    invoice_address_country = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return '%s at %s' % (self.company.name, self.fair.name)


# Work field that an exhibitor operates in
class WorkField(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Job type that an exhibitor offers
class JobType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Continent that an exhibitor operates in
class Continent(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Value or work environment that an exhibitor has
class Value(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Info about an exhibitor to be displayed in apps and on website
class CatalogInfo(models.Model):
    exhibitor = models.OneToOneField(
            Exhibitor,
            on_delete=models.CASCADE,
            primary_key=True,
            )
    display_name = models.CharField(max_length=64)
    slug = models.SlugField(db_index=False, blank=True)
    short_description = models.CharField(max_length=64)
    description = models.TextField()
    employees_sweden = models.IntegerField(default=0)
    employees_world = models.IntegerField(default=0)
    countries = models.IntegerField(default=0)
    website_url = models.CharField(max_length=128, blank=True)
    facebook_url = models.CharField(max_length=128, blank=True)
    twitter_url = models.CharField(max_length=128, blank=True)
    linkedin_url = models.CharField(max_length=128, blank=True)

    # Image fields
    # Field with name ending with original serves as the original uploaded
    # image and should be the only image uploaded,
    # the others are auto generated
    logo_original = models.ImageField(
            upload_to=UploadToDirUUID('exhibitors', 'logo_original'),
            blank=True,
            )
    logo_small = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'logo_small'), blank=True)
    logo = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'logo'), blank=True)

    ad_original = models.ImageField(
            upload_to=UploadToDirUUID('exhibitors', 'ad'), blank=True)
    ad = models.ImageField(
            upload_to=UploadToDir('exhibitors', 'ad'), blank=True)

    # ManyToMany relationships
    programs = models.ManyToManyField('people.Programme', blank=True)
    main_work_field = models.ForeignKey(
            WorkField, blank=True, null=True, related_name='+')
    work_fields = models.ManyToManyField(
            WorkField, blank=True, related_name='+')
    job_types = models.ManyToManyField(JobType, blank=True)
    continents = models.ManyToManyField(Continent, blank=True)
    values = models.ManyToManyField(Value, blank=True)

    def __str__(self):
        return self.display_name

    # Override default save method to automatically generate associated images
    # if the original has been changed
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.display_name)
        super(CatalogInfo, self).save(*args, **kwargs)
        if should_generate(self.logo_original, self.logo):
            if self.logo:
                os.remove(os.path.join(MEDIA_ROOT, self.logo.name))
                os.remove(os.path.join(MEDIA_ROOT, self.logo_small.name))
            path = os.path.join(MEDIA_ROOT, self.logo_original.name)
            self.logo_small = format_png(path, 200, 200)
            self.logo = format_png(path, 400, 400)
        if should_generate(self.ad_original, self.ad):
            if self.ad:
                os.remove(os.path.join(MEDIA_ROOT, self.ad.name))
            path = os.path.join(MEDIA_ROOT, self.ad_original.name)
            self.ad = format_jpg(path, 640, 480)
        super(CatalogInfo, self).save(*args, **kwargs)
