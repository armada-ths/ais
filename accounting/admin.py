from django.contrib import admin

from .models import *


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "description", "fair"]
    list_filter = ["fair__year"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name"]
    list_filter = ["fair__year"]


@admin.register(RegistrationSection)
class RegistrationSectionAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ["revenue", "category", "name"]
    list_display = ["name", "revenue", "registration_section", "category"]
    list_filter = ["revenue", "category", "registration_section", "revenue__fair__year"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("amount",)
    list_display = ["name", "purchasing_company", "product", "quantity", "amount"]
    list_filter = ["purchasing_company__name"]

    def amount(self, obj):
        if obj.unit_price:
            return "%s (D)" % obj.unit_price
        else:
            return obj.product.unit_price * obj.quantity
