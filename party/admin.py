from improved_admin import ModelAdminImproved
from party.models import Party
from django.contrib import admin

@admin.register(Party)
class PartyAdmin(ModelAdminImproved):
    search_fields = ("name",)
    ordering = ("name",)
    
#admin.site.register(Party)