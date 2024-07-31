from django.urls import reverse


def lunch_ticket(lunch_ticket):
    data = {
        "id": lunch_ticket.pk,
        "name": (
            lunch_ticket.user.get_full_name()
            if lunch_ticket.user
            else lunch_ticket.company.name
        ),
        "email_address": (
            lunch_ticket.user.email if lunch_ticket.user else lunch_ticket.email_address
        ),
        "comment": lunch_ticket.comment,
        "date": (
            lunch_ticket.time.__str__()
            if lunch_ticket.time
            else lunch_ticket.day.__str__()
        ),
        "used": lunch_ticket.used,
        "type": lunch_ticket.get_ticket_type(),
        "token": lunch_ticket.token,
        "dietary_restrictions": [
            dietary_restriction.name
            for dietary_restriction in lunch_ticket.dietary_restrictions.all()
        ],
        "other_dietary_restrictions": lunch_ticket.other_dietary_restrictions,
    }

    return data


def lunch_ticket_react(request, lunch_ticket):
    data = {
        "id": lunch_ticket.pk,
        "name": (
            lunch_ticket.user.get_full_name()
            if lunch_ticket.user
            else lunch_ticket.company.name
        ),
        "email_address": (
            lunch_ticket.user.email if lunch_ticket.user else lunch_ticket.email_address
        ),
        "comment": lunch_ticket.comment,
        "day": lunch_ticket.day.__str__(),
        "time": (
            lunch_ticket.time.__str__().split(" ")[1]
            if len(lunch_ticket.time.__str__().split(" ")) > 1
            else lunch_ticket.time.__str__()
        ),
        "used": lunch_ticket.used,
        "type": lunch_ticket.get_ticket_type(),
        "token": lunch_ticket.token,
        "url": request.build_absolute_uri(
            reverse("lunchticket_display", args=[lunch_ticket.token])
        ),
        "sent": lunch_ticket.sent,
        "dietary_restrictions": [
            dietary_restriction.name
            for dietary_restriction in lunch_ticket.dietary_restrictions.all()
        ],
        "other_dietary_restrictions": lunch_ticket.other_dietary_restrictions,
    }

    return data


def banquet_participant(banquet_participant):
    data = {
        "id": banquet_participant.pk,
        "token": str(banquet_participant.token),
        "title": banquet_participant.banquet.name,
        "dietary_restrictions": [
            dietary_restriction.name
            for dietary_restriction in banquet_participant.dietary_restrictions.all()
        ],
        "other_dietary_restrictions": banquet_participant.other_dietary_restrictions,
    }

    return data
