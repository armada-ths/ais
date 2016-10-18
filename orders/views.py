from django.shortcuts import render

from fair.models import Fair
from .models import Product
from django.http import HttpResponseForbidden
from fair.templatetags.fair_tags import is_armada_member

# Create your views here.
def products(request, template_name='orders/products.html'):
	if not is_armada_member(request.user):
		return HttpResponseForbidden()
	products = Product.objects.filter(fair=Fair.objects.get(name='Armada 2016'))
	return render(request, template_name, {
		'products': products,
		'total_revenue': sum([product.revenue() for product in products])
	})