from django.contrib import admin

from .models import *

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
	ordering = ('name',)
	list_display = ('fair', 'name',)
	list_filter = ('fair__year',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	ordering = ('name',)
	list_display = ('name',)
	list_filter = ('fair__year',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	ordering = ('revenue', 'category', 'name',)
	list_display = ('name', 'revenue', 'category',)
	list_filter = ('revenue', 'category', 'revenue__fair__year',)
