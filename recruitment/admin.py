from django.contrib import admin

from recruitment.admin_filters import SortedRecruitmentPeriod
from .models import *
import django.forms as forms
from improved_admin import ModelAdminImproved, SortedFairYear
from django.contrib.admin.sites import AdminSite


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
    def __init__(self, model, admin_site: AdminSite | None):
        super().__init__(model, admin_site)
        self.search_fields = ["user__first_name", "user__last_name"]

    inlines = [RoleApplicationInline]


@admin.register(Role)
class RoleAdmin(ModelAdminImproved):
    list_display = ["name", "organization_group", "recruitment_period"]
    list_filter = [SortedRecruitmentPeriod, "organization_group"]


@admin.register(Slot)
class SlotAdmin(ModelAdminImproved):
    list_display = ["__str__", "location", "recruitment_period"]
    list_filter = ["location", "recruitment_period"]


@admin.register(RecruitmentPeriod)
class RecruitmentPeriodModelAdmin(ModelAdminImproved):
    list_display = ["__str__"]
    list_filter = [SortedFairYear]


admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(CustomFieldAnswer)
admin.site.register(CustomFieldArgument)
admin.site.register(Location)
