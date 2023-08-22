from django.contrib import admin

from .models import Product, Order, ProductType, StandArea
from improvedAdmin import ModelAdminImproved


@admin.register(Order)
class OrderAdmin(ModelAdminImproved):
    """Orders are ordered by fair in first hand, then by exhibitor name. It's possible to filter order by product fair, and search for exhibitor name and product name"""

    search_fields = ("exhibitor__company__name", "product__name")
    ordering = (
        "product__fair",
        "exhibitor__company__name",
    )
    list_filter = ("product__fair__year",)


@admin.register(Product)
class ProductAdmin(ModelAdminImproved):
    search_fields = ("name",)
    ordering = (
        "-fair__year",
        "name",
    )
    list_filter = ("fair",)


# admin.site.register(Product)
# admin.site.register(Order)

@admin.register(ProductType)
class ProductTypeAdmin(ModelAdminImproved):
    pass

@admin.register(StandArea)
class StandAreaAdmin(ModelAdminImproved):
    pass
