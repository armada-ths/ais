from django.contrib import admin

from .models import Product, Order, ProductType, StandArea

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Orders are ordered by fair in first hand, then by exhibitor name. It's possible to filter order by product fair, and search for exhibitor name and product name"""
    search_fields = ('exhibitor__company__name', 'product__name')
    ordering = ('product__fair', 'exhibitor__company__name',)
    list_filter = ('product__fair__year', )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('-fair__year', 'name',)
    list_filter = ('fair', )

#admin.site.register(Product)
#admin.site.register(Order)
admin.site.register(ProductType)
admin.site.register(StandArea)
