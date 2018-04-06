from django.contrib import admin

from .models import *

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
	ordering = ("name",)
	list_display = ("fair", "name",)
	list_filter = ("fair__year",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	ordering = ("revenue", "name",)
	list_display = ("revenue", "name",)
	list_filter = ("revenue__fair__year",)
