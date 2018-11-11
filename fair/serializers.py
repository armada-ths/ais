def lunch_ticket(lunch_ticket):
    data = {
        'id': lunch_ticket.pk,
        'company': lunch_ticket.company.name,
        'email_address': lunch_ticket.email_address,
        'name': lunch_ticket.user.get_full_name() if lunch_ticket.user else None,
        'comment': lunch_ticket.comment,
        'day': lunch_ticket.day.date if lunch_ticket.day else None,
        'used': lunch_ticket.used,
        'dietary_restrictions': [diet.name for diet in lunch_ticket.dietary_restrictions.all()]
    }

    return data
