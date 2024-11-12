from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import (
    Event,
    Participant,
    SignupQuestionAnswer,
    SignupQuestionAnswerFile,
    Team,
    TeamMember,
    SignupQuestion,
    ParticipantCheckIn,
)
from improved_admin import ModelAdminImproved


@admin.register(Participant)
class ParticipantAdmin(ModelAdminImproved):
    list_display = ["__str__", "event", "in_waiting_list"]
    list_filter = ["event__fair", "event", "in_waiting_list"]

    def get_queryset(self, request):
        # this function to see participants AND waiting list participants.
        queryset = Participant.objects_all.all()
        return queryset


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


@admin.register(SignupQuestionAnswer)
class SignupQuestionAnswerAdmin(ModelAdminImproved):
    pass


@admin.register(SignupQuestionAnswerFile)
class SignupQuestionAnswerFileAdmin(ModelAdminImproved):
    pass


@admin.register(ParticipantCheckIn)
class ParticipantCheckInAdmin(ModelAdminImproved):
    pass
