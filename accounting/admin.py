from django.contrib import admin

from .models import *

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
	ordering = ['name']
	list_display = ['fair', 'name']
	list_filter = ['fair__year']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	ordering = ['name']
	list_display = ['name']
	list_filter = ['fair__year']

@admin.register(RegistrationSection)
class CategoryAdmin(admin.ModelAdmin):
	ordering = ['name']
	list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	ordering = ['revenue', 'category', 'name']
	list_display = ['name', 'revenue', 'registration_section', 'category']
	list_filter = ['revenue', 'category', 'registration_section', 'revenue__fair__year']

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter = ['purchasing_company__name']
