from django.contrib import admin

from .models import Event, Participant, Team, TeamMember, SignupQuestion, ParticipantCheckIn

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(SignupQuestion)
admin.site.register(ParticipantCheckIn)
