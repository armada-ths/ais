from django.contrib import admin
from .models import Fair, FairDay, Partner, Tag, OrganizationGroup, LunchTicketTime, LunchTicket

admin.site.register(Fair)
admin.site.register(Partner)
admin.site.register(Tag)
admin.site.register(OrganizationGroup)
admin.site.register(LunchTicketTime)
admin.site.register(LunchTicket)
