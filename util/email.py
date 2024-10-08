from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


default_context = {
    "support_email": "support@armada.nu",
}


def send_mail(
    request,
    template,
    context={},
    subject="Armada Information",
    to=[],
    file_paths=[],
):
    armada_logo_url = request.build_absolute_uri(
        "/static/images/armada_logo_text_left_green_contained.png"
    )

    context = {"armada_logo_url": armada_logo_url, **default_context, **context}

    html_content = render_to_string(template, context, request=request)
    plain_message = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        "THS Armada <noreply@armada.nu>",
        to,
    )

    for file_path in file_paths:
        try:
            email.attach_file(file_path)
        except Exception as e:
            print("Failed to attach file: ", e)

    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
    except Exception as e:
        print("Failed to send email: ", e)
        raise e
