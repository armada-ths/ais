from fair.models import Fair
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from fair.models import Fair
from django.contrib.auth.decorators import permission_required

# Create your views here.
@permission_required('products.base')
def products(request, year, template_name='orders/products.html'):
    if not request.user.has_perm('orders.view_products'):
        raise PermissionDenied
    fair = get_object_or_404(Fair, year=year)
    products = Product.objects.filter(fair=fair)
    return render(request, template_name, {
        'product_categories': [
            {'products': products, 'id': 'total_products', 'name': 'Total'},
            {'products': products.exclude(coa_number=3511), 'id': 'fair_products', 'name': 'Fair'},
            {'products': products.filter(coa_number=3511), 'id': 'banquet_products', 'name': 'Banquet'}],
        'fair': fair
    })


# Create your views here.
@permission_required('products.base')
def product(request, year, pk, template_name='orders/product.html'):
    if not request.user.has_perm('orders.view_products'):
        raise PermissionDenied
    fair = get_object_or_404(Fair, year=year)
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {
        'product': product,
        'fair': fair
    })
