from django.contrib import admin

from .models import Product, Order, ProductType

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductType)
# Register your models here.
