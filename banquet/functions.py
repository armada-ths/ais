from django.urls import reverse
from django.core.mail import send_mail


def send_invitation_mail(invitation, name, date, location, link, email):
    """Send banquet invitation mail"""
    send_mail(
        "Your invite to the banquet",
        "Hello "
        + name
        + "!\n"
        + "You have been invited to the Grand Banquet of THS Armada.\n"
        + "The banquet takes place "
        + str(date)
        + " at "
        + str(location)
        + ". \n Access your invitation with the following link:\n"
        + link
        + "\n\nSee you at the banquet!\b",
        +"Best Regards,\n",
        +"The Banquet Team of THS Armada 2023",
        "Armada Banquet <noreply@armada.nu>",
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
