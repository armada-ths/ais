from django.contrib import admin

from .models import Company, Contact, InvoiceDetails

class InvoiceInline(admin.StackedInline):
    model = InvoiceDetails


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [InvoiceInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('active',)
