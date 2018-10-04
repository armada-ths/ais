from django.urls import reverse

"""
Responsible for serializing Event modules into JSON objects
"""


def event(event, request):
    signup_location = reverse('events:event_signup', args=[event.fair.year, event.pk])
    signup_url = request.build_absolute_uri(signup_location)

    data = {
        'id': event.pk,
        'name': event.name,
        'description': event.description,
        'location': event.location,
        'event_start': int(event.date_start.strftime('%s')),
        'event_end': int(event.date_end.strftime('%s')),
        'registration_end': int(event.date_start.strftime('%s')),
        'image_url': '//archive.kottnet.net/pictures/armada%20run.png',
        'fee': event.fee_s,
        'registration_required': True,
        'external_event_link': event.external_event_link,
        'signup_questions': [signup_question(question) for question in event.signupquestion_set.all()],
        'signup_link': signup_url,
    }

    return data


def signup_question(signup_question):
    data = {
        'id': signup_question.pk,
        'type': signup_question.type,
        'question': signup_question.question,
        'required': signup_question.required,
        'options': signup_question.options,
    }

    return data


def team(team):
    data = {
        'id': team.pk,
        'name': team.name,
        'capacity': team.max_capacity,
        'leader': team.leader.get_full_name() if team.leader is not None else None,
        'members': [member.participant.__str__() for member in team.teammember_set.all()],
        'number_of_members': team.number_of_members()
    }

    return data


def participant(participant):
    data = {
        'fee_payed': participant is not None and participant.fee_payed_s,
        'signup_complete': participant is not None and participant.signup_complete
    }

    return data
