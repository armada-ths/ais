from django.contrib import admin
from django.http import HttpResponse

from orders.models import Order, Product
from .models import *


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
	search_fields = ['company__name']
	ordering = ['-fair__year', 'company']
	list_filter = ['fair']


admin.site.register(CatalogueIndustry)
admin.site.register(CatalogueValue)
admin.site.register(CatalogueEmployment)
admin.site.register(CatalogueLocation)
admin.site.register(CatalogueBenefit)
admin.site.register(LunchTicketDay)
admin.site.register(LunchTicket)
admin.site.register(Location)
admin.site.register(Booth)
admin.site.register(ExhibitorInBooth)
