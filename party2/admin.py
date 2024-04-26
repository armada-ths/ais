from django.contrib import admin
from .models import party
from improved_admin import ModelAdminImproved

@admin.register(party)
class PartyAdmin(ModelAdminImproved):
    search_fields = ("namn",)
    ordering = ("namn",)


