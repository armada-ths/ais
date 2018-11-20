def ticket(participant):
    data = {
        'id': participant.pk,
        'seat': participant.seat.name,
        'table': participant.seat.table.name,
        'name': participant.user.get_full_name() if participant.user else participant.name,
        'ticket_scanned': participant.ticket_scanned
    }

    return data
