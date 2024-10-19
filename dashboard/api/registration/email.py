import datetime

from ais.common import settings
from util.email import send_mail


def send_ir_confirmation_email(
    request,
    fair,
    signature,
    company,
    # How many days the company has to change their initial registration application after signing the contract
    ir_application_change_allowed_time=14,
    # How many days after the initial registration end date the company will receive a confirmation email
    ir_application_review_time=14,
):
    # The deadline for the company to change their initial registration application
    # either x days after signature, or the registration end date, whichever comes last.
    ir_application_change_deadline = max(
        [
            signature.timestamp
            + datetime.timedelta(days=ir_application_change_allowed_time),
            fair.registration_end_date,
        ]
    )

    # The latest date the company will receive a confirmation email
    ir_application_review_date = fair.registration_end_date + datetime.timedelta(
        days=ir_application_review_time
    )

    send_mail(
        request,
        template="register/email/ir_complete.html",
        context={
            "company": company,
            "fair": fair,
            "signature": signature,
            "ir_application_change_deadline": ir_application_change_deadline,
            "ir_application_review_date": ir_application_review_date,
            "support_email": "sales@armada.nu",
        },
        subject="Initial registration received!",
        to=[signature.company_contact.email_address],
        file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
    )


def send_cr_confirmation_email(request, fair, company, exhibitor, signature):
    # Untested
    # Todo: Add packages to email
    send_mail(
        request,
        template="register/email/cr_complete.html",
        context={
            "company": company,
            "fair": fair,
            "signature": signature,
            "deadline": exhibitor.deadline_complete_registration
            or fair.complete_registration_close_date,
        },
        subject="Final registration received!",
        to=[signature.company_contact.email_address],
        file_paths=[settings.MEDIA_ROOT + signature.contract.contract.url[6:]],
    )
