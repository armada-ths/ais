from django.shortcuts import render
from django.shortcuts import get_object_or_404
#from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from fair.models import Fair
from companies.models import Company
from register.models import SignupLog
from accounting.models import Order

# This app is used to test functionality in production without making it accesible via the rest of the site (only via the url).

def testpage(request):

    return render(request, 'testpage/testpage.html')


def send_test_email(request):

    company = get_object_or_404(Company, name='Sales Company 2')
    fair = get_object_or_404(Fair, year=2019)

    signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'INITIAL').first()
    # orders = Order.objects.filter(purchasing_company = company, unit_price = None, name = None)
    # orders_total = 10000 # dummy

    orders = []
    orders_total = 0

    # for order in Order.objects.filter(product__revenue__fair = fair, purchasing_company = company):
    #     unit_price = order.product.unit_price if order.unit_price is None else order.unit_price
    #     orders_total += order.quantity * unit_price
    #
    #     orders.append(
	# 	{
	# 		'category': order.product.category.name if order.product.category else None,
	# 		'name': order.product.name if order.name is None else order.name,
	# 		'description': order.product.description if order.product.registration_section is None else None,
	# 		'quantity': order.quantity,
	# 		'unit_price': unit_price
	# 	})

    send_CR_confirmation_email(signature, orders, orders_total)

    return render(request, 'testpage/testpage.html')


def send_CR_confirmation_email(signature, orders, orders_total):

    order_html_rows = []
    order_plain_rows = []

    for order in orders:
        if order['category']:
            product = order['category'] + ' - ' + order['name']
        else:
            product = order['name']

        html_row = '''  <tr>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						</tr>
                    ''' % (product, str(order['quantity']), str(order['unit_price']), str(int(order['quantity'])*int(order['unit_price'])))

        plain_row = '%s --- %s --- %s --- %s' % (product, order['quantity'], order['unit_price'], str(int(order['quantity'])*int(order['unit_price'])))

        order_html_rows.append(html_row)
        order_plain_rows.append(plain_row)

    order_html_rows.append('''  <tr>
                    <td>Banquet ticket</td>
                    <td>4</td>
                    <td>2000</td>
                    <td>8000</td>
                    </tr>
                ''')

    order_plain_rows.append('Banquet ticket --- 4 --- 2000 --- 8000')

    html_message = '''
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
        			Please note that this is an automatically generated email. If you have any questions please contact your sales contact person. For contact information, please visit <a href="https://armada.nu/contact/">armada.nu/contact</a>.
        		</div>
        		<div>
        			<br/>
        			Your current order contains the products listed below.
        			<br/>
        			Total amount: SEK %s
        			<br/>
        			To view or update your choices go to <a href="https://ais.armada.nu/register/">register.armada.nu</a>.
        			<br/><br/>
        			<table align="left" border="1" cellpadding="1" cellspacing="0" style="width:600px">
        				<thead>
        					<tr>
        						<th scope="col">Product</th>
        						<th scope="col">Quantity</th>
        						<th scope="col">Unit price (SEK)</th>
        						<th scope="col">Product total (SEK)</th>
        					</tr>
        				</thead>
        				<tbody>
        					%s
        				</tbody>
        			</table>
        		</div>
        	</body>
        </html>
		''' % 	(
				str(signature.company_contact),
				str(signature.timestamp.strftime('%Y-%m-%d (%H:%M)')),
				str(signature.company),
				str(orders_total),
				''.join(order_html_rows)
				)

    plain_text_message = '''Thank you for submitting the complete registration for THS Armada 2019. The complete registration contract was signed by %s on the %s for %s.

Please note that this is an automatically generated email. If you have any questions please contact your sales contact person. For contact information, please visit https://armada.nu/contact/.

Your current order contains the products listed below.
Total amount: SEK %s
To view or update your choices go to https://register.armada.nu.

Product --- Quantity --- Unit price (SEK) --- Product total (SEK)
%s
''' % 	(
				str(signature.company_contact),
				str(signature.timestamp.strftime('%Y-%m-%d (%H:%M)')),
				str(signature.company),
				str(orders_total),
				'\n'.join(order_plain_rows),
				)

    email = EmailMultiAlternatives(
        'Registration for THS Armada 2019',
        plain_text_message,
        'info@armada.nu',
        ['noreply@armada.nu'],
        #bcc = [],
    )

    email.attach_alternative(html_message, 'text/html')

    # email = EmailMessage(
	# 	subject = 'Registration for THS Armada 2019',
	# 	body = html_message,
	# 	from_email = 'info@armada.nu',
	# 	to = [signature.company_contact.email_address],
	# 	# bcc = [],
	# )
    # email.content_subtype = 'html'

    file_path = 'https://ais.armada.nu' + signature.contract.contract.url
    print("Contract path: ", file_path)
    email.attach_file(file_path)

    email.send()
