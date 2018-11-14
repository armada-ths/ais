from django.contrib import admin
from .models import Banquet, Participant, InvitationGroup, Invitation, Table, Seat, AfterPartyTicket


admin.site.register(Banquet)
admin.site.register(Participant)
admin.site.register(InvitationGroup)
admin.site.register(Invitation)
admin.site.register(Table)
admin.site.register(Seat)
admin.site.register(AfterPartyTicket)
