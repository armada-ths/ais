from django.shortcuts import render

from fair.models import Fair
from .models import Product

# Create your views here.
def products(request, template_name='orders/products.html'):
	return render(request, template_name, {
		'products': Product.objects.filter(fair=Fair.objects.get(name='Armada 2016'))
	})