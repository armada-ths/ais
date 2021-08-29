from fair.forms import LunchTicketForm
from fair.selectors import get_users_from_organization_group




def send_lunch_ticket(lunch_ticket, user):
    eat_by = str(lunch_ticket.time) if lunch_ticket.time else str(lunch_ticket.day)
    email_address = lunch_ticket.user.email if lunch_ticket.user else lunch_ticket.email_address
    send_mail(f'Lunch ticket {eat_by}',
            f'Open the link below to redeem your lunch ticket at {lunch_ticket.fair.name} \n\nDate: {eat_by} \n' +
            request.build_absolute_uri(reverse('lunchticket_display', args = ['lunchticket_display', args =
                [lunch_ticket.token])),
            'noreply@armada.nu',
            [email_address],
            fail_silently = True)

    LunchTicketSend(lunch_ticket=lunch_ticket, user=request.user, email_address=email_address).save()

    lunch_ticket.sent = True
    lunch_ticket.save()

    return lunch_ticket.token




def create_lunch_ticket_form(fair):
    form = LunchTicketForm(request.POST or None, initial={'fair': fair})
    users = get_users_from_organization_group(fair=fair)
    form.fields['user'].choices = [('', '---------')] + users

    return form
