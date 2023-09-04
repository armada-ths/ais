from django.contrib import admin
from .models import *
import django.forms as forms
from improvedAdmin import ModelAdminImproved


class CustomFieldInline(admin.TabularInline):
    model = CustomField


class CustomFieldAnswerInline(admin.TabularInline):
    model = CustomFieldAnswer


class CustomFieldArgumentInline(admin.TabularInline):
    model = CustomFieldArgument


class CustomFieldAdmin(ModelAdminImproved):
    inlines = [CustomFieldArgumentInline]


class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication


class RecruitmentApplicationAdmin(ModelAdminImproved):
    inlines = [RoleApplicationInline]


@admin.register(Role)
class RoleAdmin(ModelAdminImproved):
    list_display = ["name", "organization_group", "recruitment_period"]
    list_filter = ["recruitment_period", "organization_group"]


@admin.register(Slot)
class SlotAdmin(ModelAdminImproved):
    list_display = ["__str__", "location", "recruitment_period"]
    list_filter = ["location", "recruitment_period"]


@admin.register(RecruitmentPeriod)
class RecruitmentPeriodModelAdmin(ModelAdminImproved):
    pass


admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(CustomFieldAnswer)
admin.site.register(CustomFieldArgument)
admin.site.register(Location)
