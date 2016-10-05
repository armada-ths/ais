from django.db import models
#from lib.image import random_path, format_png, format_jpg
from django.conf import settings
from django.contrib.auth.models import User
import os


MEDIA_ROOT = settings.MEDIA_ROOT


class ExhibitorLocation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
    company = models.ForeignKey('companies.Company')
    fair = models.ForeignKey('fair.Fair')
    responsible = models.ForeignKey(User, null=True, default=None, blank=True)
    location =  models.ForeignKey(ExhibitorLocation, null=True, default=None, blank=True)

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

# Since these functions break when running makemigrations temporary dummy implenetations are provided!
def random_path(a,b):
    return ""

def format_png():
    return None

# Info about an exhibitor to be displayed in apps and on website
class CatalogInfo(models.Model):
    exhibitor = models.OneToOneField(Exhibitor, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64)
    slug = models.SlugField(db_index=False)
    short_description = models.CharField(max_length=64)
    description = models.TextField()
    employees_sweden = models.IntegerField()
    employees_world = models.IntegerField()
    countries = models.IntegerField()
    website_url = models.CharField(max_length=128, blank=True)
    facebook_url = models.CharField(max_length=128, blank=True)
    twitter_url = models.CharField(max_length=128, blank=True)
    linkedin_url = models.CharField(max_length=128, blank=True)

    # Images
    logo_small = models.ImageField(
            upload_to=random_path('exhibitors', 'logo_small'), blank=True)
    logo = models.ImageField(
            upload_to=random_path('exhibitors', 'logo'), blank=True)
    ad = models.ImageField(
            upload_to=random_path('exhibitors', 'ad'), blank=True)

    programs = models.ManyToManyField('people.Programme', blank=True)
    main_work_field = models.ForeignKey(
            WorkField, blank=True, null=True, related_name='+')
    work_fields = models.ManyToManyField(
            WorkField, blank=True, related_name='+')
    job_types = models.ManyToManyField(JobType, blank=True)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        super(CatalogInfo, self).save(*args, **kwargs)
        if self.logo:
            path = os.path.join(MEDIA_ROOT, self.logo.name)
            self.logo_small = format_png(path, 128, 128)
            self.logo = format_png(path, 400, 400)
        if self.ad:
            path = os.path.join(MEDIA_ROOT, self.ad.name)
            self.ad = format_jpg(path, 640, 480)
        super(CatalogInfo, self).save(*args, **kwargs)
