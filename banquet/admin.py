from django.contrib import admin
from .models import Banquet, Participant, InvitationGroup, Invitation, Table, Seat, AfterPartyInvitation, AfterPartyTicket, TableMatching


admin.site.register(Banquet)
admin.site.register(Participant)
admin.site.register(InvitationGroup)
admin.site.register(Invitation)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
	list_filter = ['table__banquet']

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
	list_filter = ['banquet']

@admin.register(TableMatching)
class TableMatchingAdmin(admin.ModelAdmin):
    list_filter = ['participant__banquet']

@admin.register(AfterPartyInvitation)
class AfterPartyInvitationAdmin(admin.ModelAdmin):
	list_filter = ['banquet']
	ordering = ['name', 'email_address']

@admin.register(AfterPartyTicket)
class AfterPartyTicketAdmin(admin.ModelAdmin):
	list_filter = ['banquet', 'has_paid']
	list_display = ['name', 'email_address', 'has_paid']
