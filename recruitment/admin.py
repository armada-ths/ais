from django.contrib import admin
from .models import *
import django.forms as forms


class CustomFieldInline(admin.TabularInline):
    model = CustomField


class CustomFieldAnswerInline(admin.TabularInline):
    model = CustomFieldAnswer


class CustomFieldArgumentInline(admin.TabularInline):
    model = CustomFieldArgument


class CustomFieldAdmin(admin.ModelAdmin):
    inlines = [CustomFieldArgumentInline]


class RoleApplicationInline(admin.TabularInline):
    model = RoleApplication


class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "organization_group", "recruitment_period"]
    list_filter = ["recruitment_period", "organization_group"]


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["__str__", "location", "recruitment_period"]
    list_filter = ["location", "recruitment_period"]

@admin.register(RecruitmentPeriod)
class RecruitmentPeriodModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }

admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(CustomFieldAnswer)
admin.site.register(CustomFieldArgument)
admin.site.register(Location)
