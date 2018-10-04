from django.contrib import admin

from .models import Event, Participant, Team, TeamMember, SignupQuestion

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(SignupQuestion)
