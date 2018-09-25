from django.urls import reverse


def event(event, request):
    signup_location = reverse('events:event_signup', args=[event.fair.year, event.pk])
    signup_url = request.build_absolute_uri(signup_location)

    data = {
        'id': event.pk,
        'name': event.name,
        'description': event.description,
        'location': event.location,
        'fee': event.fee_s,
        'external_event_link': event.external_event_link,
        'signup_questions': [signup_question(question) for question in event.signupquestion_set.all()],
        'signup_url': signup_url,
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
