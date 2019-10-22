from django.contrib import admin
from .models import Banquet, Participant, InvitationGroup, Invitation, Table, Seat, AfterPartyTicket, TableMatching


admin.site.register(Banquet)
admin.site.register(Participant)
admin.site.register(InvitationGroup)
admin.site.register(Invitation)
admin.site.register(AfterPartyTicket)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
	list_filter = ['table__banquet']

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
	list_filter = ['banquet']

@admin.register(TableMatching)
class TableMatchingAdmin(admin.ModelAdmin):
    list_filter = ['participant__banquet']
