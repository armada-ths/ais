from django import forms
from django.contrib import admin
from .models import *


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


class RecruitmentApplicationForm(forms.ModelForm):
    class Meta:
        model = RecruitmentApplication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RecruitmentApplicationForm, self).__init__(*args, **kwargs)
        self.fields["delegated_role"].queryset = Role.objects.filter(
            organization_group__fair__current=True
        )


class RecruitmentApplicationAdmin(admin.ModelAdmin):
    inlines = [RoleApplicationInline]
    form = RecruitmentApplicationForm


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "organization_group", "recruitment_period"]
    list_filter = ["recruitment_period", "organization_group"]


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["__str__", "location", "recruitment_period"]
    list_filter = ["location", "recruitment_period"]


admin.site.register(RecruitmentPeriod)
admin.site.register(RecruitmentApplication, RecruitmentApplicationAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(CustomFieldAnswer)
admin.site.register(CustomFieldArgument)
admin.site.register(Location)
