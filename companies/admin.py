from django.contrib import admin

from .models import *

from improvedAdmin import ModelAdminImproved

class CompanyAddressInline(admin.StackedInline):
    model = CompanyAddress


class CompanyLogInline(admin.StackedInline):
    model = CompanyLog


@admin.register(Group)
class GroupAdmin(ModelAdminImproved):
    ordering = (
        "fair__year",
        "parent__name",
        "name",
    )
    list_display = (
        "fair",
        "__str__",
    )
    list_filter = ("fair__year",)


@admin.register(CompanyContact)
class CompanyContactAdmin(ModelAdminImproved):
    ordering = (
        "first_name",
        "last_name",
    )
    search_fields = (
        "company__name",
        "first_name",
        "last_name",
    )


@admin.register(Company)
class CompanyAdmin(ModelAdminImproved):
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [CompanyAddressInline, CompanyLogInline]

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user.id
        super(CompanyAdmin, self).save_model(request, obj, form, change)


@admin.register(CompanyType)
class CompanyTypeAdmin(ModelAdminImproved):
    ordering = ("type",)


@admin.register(CompanyCustomer)
class CompanyCustomerAdmin(ModelAdminImproved):
    ordering = (
        "fair__year",
        "company__name",
    )
    list_display = (
        "fair",
        "company",
    )
    list_filter = ("fair__year",)
