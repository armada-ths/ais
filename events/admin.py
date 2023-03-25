from django.contrib import admin

from .models import (
    Event,
    Participant,
    Team,
    TeamMember,
    SignupQuestion,
    ParticipantCheckIn,
)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["__str__", "event"]
    list_filter = ["event__fair", "event"]


admin.site.register(Event)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(SignupQuestion)
admin.site.register(ParticipantCheckIn)
