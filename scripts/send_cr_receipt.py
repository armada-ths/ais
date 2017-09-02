'''
This scritp sends an email to the contacts of all exhibitors (in current fair) with their orders
'''

from exhibitors.models import Exhibitor
from companies.models import Contact
from django.core.mail import send_mail
from orders.models import Order, Product
from fair.models import Fair
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
import logging


fair = Fair.objects.filter(current=True)			
exhibitors = Exhibitor.objects.filter(fair=fair)
products = Product.objects.filter(fair=fair)

for exhibitor in exhibitors:
	try:
		contact_email = exhibitor.contact.email
	except:
		logging.error("No contact for this exhibitor")
		continue

	orders =  Order.objects.filter(exhibitor = exhibitor)
	total_price = 0


	orders_info = []
	#Go thrue orders and get the total price for everything and place the important info as a dictionary in the list orders_info
	for o in orders:
		product = o.product
		price = product.price
		amount = o.amount
		total_price += price*amount

		order = {'product' : product.name, 'price' : product.price*amount, 'amount' : o.amount} 
		orders_info.append(order)


	send_mail(
		'Your orders for Armada',
		get_template('exhibitors/send_cr_receipt.html').render(({
			'orders_info' : orders_info,
			'total_price' : total_price,
			})
		),

		settings.DEFAULT_FROM_EMAIL,
		[contact_email],
		fail_silently=False)

