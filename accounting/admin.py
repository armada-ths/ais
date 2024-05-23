from django.contrib import admin

from .models import *
from improved_admin import ModelAdminImproved


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


@admin.register(Product)
class ProductAdmin(ModelAdminImproved):
    ordering = ["revenue", "category", "name"]
    list_display = ["name", "revenue", "registration_section", "category"]
    list_filter = ["revenue", "category", "registration_section", "revenue__fair__year"]


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
