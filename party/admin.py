from django.contrib import admin
from .models import Party
from improved_admin import ModelAdminImproved


@admin.register(Party)
class PartyAdmin(ModelAdminImproved):
    search_fields = ("name",)
    ordering = ("name",)
