from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from fair.models import Fair
from companies.models import Company
from register.models import SignupLog
from accounting.models import Order

# This app is used to test functionality in production without making it accesible via the rest of the site (only via the url).


def testpage(request):
    return render(request, "testpage/testpage.html")


def send_test_email(request):
    company = get_object_or_404(Company, name="Sales Company 2")
    fair = get_object_or_404(Fair, year=2019)

    signature = SignupLog.objects.filter(
        company=company, contract__fair=fair, contract__type="INITIAL"
    ).first()
    deadline = signature.timestamp

    send_CR_confirmation_email(signature, deadline)

    return render(request, "testpage/testpage.html")


def send_CR_confirmation_email(signature, deadline):
    html_message = """
		<html>
        	<body>
        		<style>
        			* {
        			  font-family: sans-serif;
        			  font-size: 12px;
        			}
        		</style>
        		<div>
        		      Thank you for submitting the complete registration for THS Armada 2019. The complete registration contract was signed by %s on the %s for %s.
                      <br/><br/>
                      The complete registration is binding and you will be liable for all additional services selected at the last date of the registration (%s), provided that THS Armada is able to supply your organization with your choices.
                      <br/><br/>
                      To view and edit your ordered products, go to <a href="https://ais.armada.nu/register/">register.armada.nu</a>. You can edit your order until the last date of the registration.
                      <br/><br/>
                      Please note that this is an automatically generated email. If you have any questions, please contact your sales contact person. For contact information, visit <a href="https://armada.nu/contact/">armada.nu/contact</a>.
        		</div>
        	</body>
        </html>
		""" % (
        str(signature.company_contact),
        str(signature.timestamp.strftime("%Y-%m-%d (%H:%M)")),
        str(signature.company),
        str(deadline.strftime("%Y-%m-%d")),
    )

    plain_text_message = """Thank you for submitting the complete registration for THS Armada 2019. The complete registration contract was signed by %s on the %s for %s.

The complete registration is binding and you will be liable for all additional services selected at the last date of the registration (%s), provided that THS Armada is able to supply your organization with your choices.

To view and edit your ordered products, go to <a href="https://ais.armada.nu/register/">register.armada.nu</a>. You can edit your order until the last date of the registration.

Please note that this is an automatically generated email. If you have any questions, please contact your sales contact person. For contact information, visit <a href="https://armada.nu/contact/">armada.nu/contact</a>.
""" % (
        str(signature.company_contact),
        str(signature.timestamp.strftime("%Y-%m-%d (%H:%M)")),
        str(signature.company),
        str(deadline.strftime("%Y-%m-%d")),
    )

    email = EmailMultiAlternatives(
        "Complete registration for THS Armada 2019",
        plain_text_message,
        "noreply@armada.nu",
        ["info@armada.nu"],
        # bcc = [],
    )
    email.attach_alternative(html_message, "text/html")

    file_path = settings.MEDIA_ROOT + signature.contract.contract.url[6:]
    email.attach_file(file_path)  # NOTE: comment out if run locally

    email.send()
