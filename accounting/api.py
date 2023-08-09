from rest_framework import serializers

from django.http import JsonResponse

from accounting.models import Category, Order, Product
from fair.models import Fair


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "allow_multiple_purchases")


class ProductChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "max_quantity",
            "unit_price",
            "description",
            "category",
            "no_customer_removal",
        )

    category = CategorySerializer()


class ProductSerializer(ProductChildSerializer):
    class Meta(ProductChildSerializer.Meta):
        fields = ProductChildSerializer.Meta.fields + ("child_products",)

    child_products = ProductChildSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "product", "quantity", "unit_price", "comment")

    product = ProductSerializer()


def list_products(request):
    fair = Fair.objects.get(current=True)
    products = Product.objects.filter(revenue__fair=fair)

    return JsonResponse(ProductSerializer(products, many=True).data, safe=False)
