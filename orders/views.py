from django.shortcuts import render

from fair.models import Fair
from .models import Product
from django.http import HttpResponseForbidden
from fair.templatetags.fair_tags import is_armada_member

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied


# Create your views here.
def products(request, template_name='orders/products.html'):
    if not is_armada_member(request.user):
        return HttpResponseForbidden()
    products = Product.objects.filter(fair=Fair.objects.get(name='Armada 2016'))
    return render(request, template_name, {
        'products': products,
        'total_revenue': sum([product.revenue() for product in products])
    })


# Create your views here.
def product(request, pk, template_name='orders/product.html'):
    if not is_armada_member(request.user):
        return HttpResponseForbidden()
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {
        'product': product,
    })
