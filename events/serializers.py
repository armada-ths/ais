from django.urls import reverse

"""
Responsible for serializing Event modules into JSON objects
"""


def event(event, request):
    signup_location = reverse("events:event_signup", args=[event.fair.year, event.pk])
    signup_url = request.build_absolute_uri(signup_location)

    data = {
        "id": event.pk,
        "name": event.name,
        "description": event.description,
        "location": event.location,
        "food": event.food,
        "event_start": int(event.date_start.strftime("%s")),
        "event_end": int(event.date_end.strftime("%s")),
        "event_start_string": event.date_start.strftime("%Y-%m-%d %H:%M"),
        "registration_end": (
            int(event.registration_end_date.strftime("%s"))
            if event.registration_end_date
            else None
        ),
        "image_url": (
            request.build_absolute_uri(event.picture.url) if event.picture else None
        ),
        "fee": event.fee_s,
        "registration_required": True,
        "external_event_link": event.external_event_link,
        "signup_questions": [
            signup_question(question) for question in event.signupquestion_set.all()
        ],
        "signup_link": signup_url,
        "can_create_teams": event.teams_create_s,
        "can_join_teams": event.teams_participate_s,
        "open_for_signup_student": event.open_for_signup and event.signup_s,
        "open_for_signup_company": event.open_for_signup and event.signup_cr,
        "event_max_capacity": event.event_max_capacity,
        "participant_count": event.participant_count,
    }

    return data


def signup_question(signup_question):
    data = {
        "id": signup_question.pk,
        "type": signup_question.type,
        "question": signup_question.question,
        "required": signup_question.required,
        "options": signup_question.options,
    }

    return data


def team(team):
    data = {
        "id": team.pk,
        "name": team.name,
        "capacity": team.max_capacity,
        "members": [team_member(member) for member in team.teammember_set.all()],
        "number_of_members": team.number_of_members(),
    }

    return data


def team_member(team_member):
    data = {
        "id": team_member.pk,
        "participant_id": team_member.participant.pk,
        "name": team_member.participant.__str__(),
        "leader": team_member.leader,
    }

    return data


def participant(participant):
    data = {
        "id": participant.pk,
        "name": participant.assigned_name(),
        "fee_payed": participant.fee_payed_s,
        "signup_complete": participant.signup_complete,
        "team_id": participant.team().id if participant.team() else None,
        "team_name": participant.team().name if participant.team() else None,
        "is_team_leader": participant.teammember_set.first()
        and participant.teammember_set.first().leader,
        "check_in_token": participant.check_in_token,
        "has_checked_in": participant.has_checked_in(),
    }

    return data
