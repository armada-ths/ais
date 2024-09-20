from django.contrib import admin
from .models import (
    Banquet,
    DietaryPreference,
    Participant,
    InvitationGroup,
    Invitation,
    Table,
    Seat,
    AfterPartyInvitation,
    AfterPartyTicket,
    TableMatching,
)

from improved_admin import ModelAdminImproved


@admin.register(Participant)
class ParticipantAdmin(ModelAdminImproved):
    pass


@admin.register(Banquet)
class BanquetAdmin(ModelAdminImproved):
    pass


@admin.register(InvitationGroup)
class InvitationGroupAdmin(ModelAdminImproved):
    pass


@admin.register(Invitation)
class InvitationAdmin(ModelAdminImproved):
    pass


@admin.register(Seat)
class SeatAdmin(ModelAdminImproved):
    list_filter = ["table__banquet"]


@admin.register(Table)
class TableAdmin(ModelAdminImproved):
    list_filter = ["banquet"]


@admin.register(TableMatching)
class TableMatchingAdmin(ModelAdminImproved):
    list_filter = ["participant__banquet"]


@admin.register(AfterPartyInvitation)
class AfterPartyInvitationAdmin(ModelAdminImproved):
    list_filter = ["banquet"]
    ordering = ["name", "email_address"]


@admin.register(AfterPartyTicket)
class AfterPartyTicketAdmin(ModelAdminImproved):
    list_filter = ["banquet", "has_paid"]
    list_display = ["name", "email_address", "has_paid"]


@admin.register(DietaryPreference)
class DietaryPreferenceAdmin(ModelAdminImproved):
    pass
