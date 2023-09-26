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

from improved_admin import ModelAdminImproved


class FairDayInlineAdmin(admin.TabularInline):
    model = FairDay


@admin.register(FairDay)
class FairDayAdmin(ModelAdminImproved):
    pass


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
    pass


@admin.register(LunchTicket)
class LunchTicketAdmin(ModelAdminImproved):
    pass


@admin.register(LunchTicketTime)
class LunchTicketTimeAdmin(ModelAdminImproved):
    pass
