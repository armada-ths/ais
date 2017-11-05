from django.contrib import admin

from .models import Company, Contact


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('active',)
