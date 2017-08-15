# This script is only made for fixing the db after a bug in 2017. The problem was that some orders was connected to an exhibior from the current year, 
# but contained products from last year. The last year exhibitor had been overwritten by the current year. This script creates a new exhibitor for the company, 
# connected to the fair 2016 (last years fair in writing moment) and connects the orders with products connected to the fair 2016, to that exhibitor.

from orders.models import Order, Product
from exhibitors.models import Exhibitor
from fair.models import Fair

not_current_products = Product.objects.filter(fair = Fair.objects.get(year = 2016))
current_exhibitor = Exhibitor.objects.filter(fair = Fair.objects.get(current = True))
faulty_orders = Order.objects.filter(exhibitor__in = current_exhibitor, product__in = not_current_products)

for o in faulty_orders:
	company = o.exhibitor.company 
	existing_exhibitor = Exhibitor.objects.filter(fair = Fair.objects.get(year = 2016), company = company)
	
	if existing_exhibitor.exists():
		last_year_exhibitor = list(existing_exhibitor)[0]
	else: 
		last_year_exhibitor = Exhibitor(fair = Fair.objects.get(year = 2016), company = company, about_text = "This exhibitor is incomplete due to a bug in 2017. The orders are complete.")
		last_year_exhibitor.save()
	o.exhibitor = last_year_exhibitor
	o.save()

	