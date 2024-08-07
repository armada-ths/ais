from datetime import datetime
from django.contrib import admin

from .models import *
from improved_admin import ModelAdminImproved
from django.utils.translation import gettext_lazy as _


class RevenueDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-fair__year")
            .values_list("fair__year", flat=True)
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
            return queryset.filter(fair__year=self.value())
        return queryset


@admin.register(Revenue)
class RevenueAdmin(ModelAdminImproved):
    ordering = ["-fair__year"]
    list_display = ["name", "description", "fair"]
    list_filter = [RevenueDescendingFilter]


class CategoryDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-fair__year")
            .values_list("fair__year", flat=True)
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
            return queryset.filter(fair__year=self.value())
        return queryset


@admin.register(Category)
class CategoryAdmin(ModelAdminImproved):
    ordering = ["name"]
    list_display = ["name"]
    list_filter = [CategoryDescendingFilter]


@admin.register(RegistrationSection)
class RegistrationSectionAdmin(ModelAdminImproved):
    ordering = ["name"]
    list_display = ["name"]


class ChildProductDescendingFilter(admin.SimpleListFilter):
    title = _("Year")
    parameter_name = "product__revenue__fair__year"

    def lookups(self, request, model_admin):
        # Retrieve all unique years from the related model and sort them in descending order
        years = (
            model_admin.model.objects.order_by("-product__revenue__fair__year")
            .values_list("product__revenue__fair__year", flat=True)
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
            return queryset.filter(product__revenue__fair__year=self.value())
        return queryset


@admin.register(ChildProduct)
class ChildProductAdmin(ModelAdminImproved):
    fields = ("child_product", "description", "quantity")
    list_filter = [ChildProductDescendingFilter]


@admin.register(SpecificProduct)
class SpecificProductAdmin(ModelAdminImproved):
    fields = ("specific_product",)


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


class OrderFairYearFilter(admin.SimpleListFilter):
    title = _("Category Fair Year")
    parameter_name = "fair_year"

    def lookups(self, request, model_admin):
        # Get distinct years directly from the database
        years = (
            Order.objects.exclude(product__isnull=True)
            .exclude(product__category__isnull=True)
            .values_list("product__category__fair__year", flat=True)
            .distinct()
        )
        return [(year, year) for year in sorted(years, reverse=True)]

    def value(self):
        # Default to the current year if no specific value is selected
        if not self.used_parameters.get(self.parameter_name):
            return str(datetime.now().year)
        return super().value()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__category__fair__year=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(ModelAdminImproved):
    readonly_fields = ("amount",)
    list_display = [
        "display_name",
        "purchasing_company",
        "product",
        "quantity",
        "amount",
        "fair_year",
    ]
    list_filter = [OrderFairYearFilter, "purchasing_company__name"]
    ordering = ["-created_at"]

    def display_name(self, obj):
        if obj.name:
            return "%s" % obj.name
        return "%s" % obj.product.name

    display_name.short_description = "Name"

    def amount(self, obj):
        if obj.unit_price:
            return "%s (D)" % obj.unit_price
        else:
            return obj.product.unit_price * obj.quantity

    def fair_year(self, obj):
        return obj.fair_year or "N/A"

    fair_year.admin_order_field = "product__category__fair__year"
    fair_year.short_description = "Category Fair Year"
