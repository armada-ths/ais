from django.contrib import admin
from .models import (
    Fair,
    FairDay,
    Partner,
    Tag,
    OrganizationGroup,
    LunchTicketTime,
    LunchTicket,
)
from django.contrib.admin.sites import AdminSite
from improved_admin import ModelAdminImproved, SortedFairYear


class FairDayInlineAdmin(admin.TabularInline):
    model = FairDay


@admin.register(FairDay)
class FairDayAdmin(ModelAdminImproved):
    # We need to override search_fields to be date instead of name.
    def __init__(self, model, admin_site: AdminSite | None):
        super().__init__(model, admin_site)
        self.search_fields = ["date"]


@admin.register(Fair)
class FairAdmin(ModelAdminImproved):
    inlines = [FairDayInlineAdmin]


@admin.register(Partner)
class PartnerAdmin(ModelAdminImproved):
    pass


@admin.register(Tag)
class TagAdmin(ModelAdminImproved):
    pass


@admin.register(OrganizationGroup)
class OrganisationGroupAdmin(ModelAdminImproved):
    list_filter = [SortedFairYear]


@admin.register(LunchTicket)
class LunchTicketAdmin(ModelAdminImproved):
    list_filter = [SortedFairYear]

    def __init__(self, model, admin_site: AdminSite | None):
        super().__init__(model, admin_site)
        self.search_fields = ["company__name"]


@admin.register(LunchTicketTime)
class LunchTicketTimeAdmin(ModelAdminImproved):
    pass
