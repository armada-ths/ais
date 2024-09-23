from django.urls import reverse

from util.email import send_mail


def send_invitation_mail(request, invitation, name, date, location, link, email, fair):
    """Send banquet invitation mail"""
    # send_mail(
    #     "Your invite to the banquet",
    #     "Hello "
    #     + str(name)
    #     + "!\n"
    #     + "You have been invited to the Grand Banquet of THS Armada.\n"
    #     + "The banquet takes place "
    #     + str(date)
    #     + " at "
    #     + str(location)
    #     + ". \nAccess your invitation with the following link:\n"
    #     + link
    #     + "\n\nSee you at the banquet!\n"
    #     + "Best Regards,\n"
    #     + "The Banquet Team of THS Armada 2023",
    #     "Armada Banquet <noreply@armada.nu>",
    #     [email],
    # )

    # invitation.has_sent_mail = True
    # invitation.save()

    try:
        send_mail(
            request,
            template="banquet/email/invitation.html",
            context={
                "name": name,
                "date": date,
                "location": location,
                "link": link,
                "year": fair.year,
            },
            subject="Initial registration received!",
            to=[email],
            # file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
        )
    except Exception as e:
        print("Failed to send email: ", e)
        return

    invitation.has_sent_mail = True
    invitation.save()


def send_confirmation_email(request, invitation, name, email_address, fair):
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
        request,
        invitation,
        name,
        banquet.date,
        banquet.location,
        link,
        email_address,
        fair,
    )
