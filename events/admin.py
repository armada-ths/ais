from django.contrib import admin

from .models import (
    Event,
    Participant,
    Team,
    TeamMember,
    SignupQuestion,
    ParticipantCheckIn,
)
from improved_admin import ModelAdminImproved


@admin.register(Participant)
class ParticipantAdmin(ModelAdminImproved):
    list_display = ["__str__", "event"]
    list_filter = ["event__fair", "event"]


@admin.register(Event)
class EventAdmin(ModelAdminImproved):
    pass


@admin.register(Team)
class TeamAdmin(ModelAdminImproved):
    pass


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdminImproved):
    pass


@admin.register(SignupQuestion)
class SignupQuestionAdmin(ModelAdminImproved):
    pass


@admin.register(ParticipantCheckIn)
class ParticipantCheckInAdmin(ModelAdminImproved):
    pass
