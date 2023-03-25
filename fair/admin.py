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


class FairDayAdmin(admin.TabularInline):
    model = FairDay


class FairAdmin(admin.ModelAdmin):
    inlines = [FairDayAdmin]


admin.site.register(Fair, FairAdmin)

admin.site.register(Partner)
admin.site.register(Tag)
admin.site.register(OrganizationGroup)
admin.site.register(LunchTicketTime)
admin.site.register(LunchTicket)
