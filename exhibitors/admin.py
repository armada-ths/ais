from django.contrib import admin
from django.http import HttpResponse

from orders.models import Order, Product
from .models import *
from improved_admin import ModelAdminImproved
from django import forms
from django.contrib.auth.admin import UserAdmin
from .forms import ExhibitorForm


@admin.register(Exhibitor)
class ExhibitorAdmin(ModelAdminImproved):
    search_fields = ["company__name"]
    ordering = ["-fair__year", "company"]
    list_filter = ["fair"]
    form = ExhibitorForm


@admin.register(CatalogueIndustry)
class CatalogueIndustryAdmin(ModelAdminImproved):
    list_display = ("industry", "category", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueCompetence)
class CatalogueCompetenceAdmin(ModelAdminImproved):
    list_display = ("competence", "category", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueValue)
class CatalogueValueAdmin(ModelAdminImproved):
    list_display = ("value", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueEmployment)
class CatalogueEmploymentAdmin(ModelAdminImproved):
    list_display = ("employment", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueLocation)
class CatalogueLocationAdmin(ModelAdminImproved):
    list_display = ("location", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueBenefit)
class CatalogueBenefitAdmin(ModelAdminImproved):
    list_display = ("benefit", "include_in_form")
    list_filter = ["include_in_form"]


@admin.register(CatalogueCategory)
class CatalogueCategoryAdmin(ModelAdminImproved):
    list_display = ["category"]


@admin.register(Location)
class LocationAdmin(ModelAdminImproved):
    pass


@admin.register(FairLocationSpecial)
class FairLocationSpecialAdmin(ModelAdminImproved):
    pass
