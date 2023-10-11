from django.urls import reverse
from django.core.mail import send_mail


def send_invitation_mail(invitation, name, date, location, link, email):
    """Send banquet invitation mail"""
    send_mail(
        "Your invite to the banquet",
        "Hello "
        + name
        + "!\n"
        + " You have been invited to the Grand Banquet of THS Armada. The banquet takes place "
        + str(date)
        + " at "
        + str(location)
        + ". \n Access your invitation with the following link: "
        + link
        + "\n\nSee you at the party!",
        "noreply@armada.nu",
        [email],
        fail_silently=True,
    )

    invitation.has_sent_mail = True
    invitation.save()


def send_confirmation_email(request, invitation, name, email_address):
    """Send banquet confirmation mail"""

    if invitation.has_sent_mail:
        print(
            "Tried sending banquet confirmation mail to: %s at address %s, but a mail has already been sent"
            % (name, email_address)
        )
        return

    print(
        "Sending banquet confirmation mail to: %s at address %s" % (name, email_address)
    )

    banquet = invitation.banquet
    token = invitation.token
    # External and internal user invitations look different
    if invitation.user is None:
        link = request.build_absolute_uri(
            reverse(
                "banquet_external_invitation",
                kwargs={"token": token},
            )
        )
    else:
        link = request.build_absolute_uri(
            reverse(
                "banquet_invitation",
                kwargs={"year": banquet.fair.year, "token": token},
            )
        )

    send_invitation_mail(
        invitation, name, banquet.date, banquet.location, link, email_address
    )


# def get_table(table_number):
#     (table, was_created) = BanquetTable.objects.get_or_create(pk=table_number)
#     if was_created:
#         table.table_name = "Table " + str(table_number)
#         table.number_of_seats = 8
#         table.save()
#     return table


# def sit_attendants():
#     """
#     A helper function that sits down BanquetAttendants at Tables (no optimisation right now)
#     """
#     table_number = 1
#     attendants_at_table = 0
#     table = get_table(table_number)
#     for attendant in BanquetteAttendant.objects.all():
#         if attendant.confirmed:
#             attendants_at_table += 1
#             if attendants_at_table > table.number_of_seats:
#                 table_number += 1
#                 table = get_table(table_number)
#                 attendants_at_table = 1
#             attendant.table = table
#             attendant.seat_number = attendants_at_table
#             attendant.save()
