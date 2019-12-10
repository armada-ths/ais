from django.contrib import admin

from django.http import HttpResponse
from .models import SignupContract, SignupLog

# Overrides admin register to add custom actions
@admin.register(SignupLog)
class SignupLogAdmin(admin.ModelAdmin):
	search_fields = ['company__name']
	ordering = ['-timestamp']
	list_filter = ['type', 'contract__fair', 'contract']

@admin.register(SignupContract)
class SignupContractAdmin(admin.ModelAdmin):
	list_display = ('name', 'fair', 'type', 'contract_company_type', 'current', 'default')
	list_filter = ['fair', 'type']
