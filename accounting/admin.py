from datetime import datetime
from django.contrib import admin

from .models import *
from improved_admin import ModelAdminImproved
from django.utils.translation import gettext_lazy as _


@admin.register(Revenue)
class RevenueAdmin(ModelAdminImproved):
    ordering = ["name"]
    list_display = ["name", "description", "fair"]
    list_filter = ["fair__year"]


@admin.register(Category)
class CategoryAdmin(ModelAdminImproved):
    ordering = ["name"]
    list_display = ["name"]
    list_filter = ["fair__year"]


@admin.register(RegistrationSection)
class RegistrationSectionAdmin(ModelAdminImproved):
    ordering = ["name"]
    list_display = ["name"]


@admin.register(ChildProduct)
class ChildProductAdmin(ModelAdminImproved):
    fields = ("child_product", "quantity")


class YearDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "revenue__fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-revenue__fair__year")
            .values_list("revenue__fair__year", flat=True)
            .distinct()
        )
        return [(year, year) for year in years]

    # Default to current year selected
    def value(self):
        # Default to the current year if no specific value is selected
        if not self.used_parameters.get(self.parameter_name):
            return str(datetime.now().year)
        return super().value()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(revenue__fair__year=self.value())
        return queryset


@admin.register(Product)
class ProductAdmin(ModelAdminImproved):
    ordering = ["-revenue__fair__year", "revenue", "category", "name"]
    list_display = ["name", "revenue", "registration_section", "category"]
    list_filter = [
        YearDescendingFilter,
        "revenue",
        "category",
        "registration_section",
    ]


@admin.register(Stock)
class StockAdmin(ModelAdminImproved):
    list_display = ["name", "amount"]


@admin.register(ExportBatch)
class ExportBatchAdmin(ModelAdminImproved):
    list_display = ["timestamp", "user"]


@admin.register(Order)
class OrderAdmin(ModelAdminImproved):
    readonly_fields = ("amount",)
    list_display = ["name", "purchasing_company", "product", "quantity", "amount"]
    list_filter = ["purchasing_company__name"]

    def amount(self, obj):
        if obj.unit_price:
            return "%s (D)" % obj.unit_price
        else:
            return obj.product.unit_price * obj.quantity
