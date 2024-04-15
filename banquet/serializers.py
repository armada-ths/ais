def ticket(participant):
    data = {
        "id": participant.pk,
        "seat": participant.seat.name if participant.seat else "",
        "table": participant.seat.table.name if participant.seat else "",
        "name": (
            participant.user.get_full_name() if participant.user else participant.name
        ),
        "ticket_scanned": participant.ticket_scanned,
    }

    return data
