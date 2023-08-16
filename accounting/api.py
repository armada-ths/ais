from util import (
    JSONError,
    get_company_contact,
    get_contract_signature,
    get_user,
    status,
)

from rest_framework import serializers

from django.db.models import Q
from django.http import JsonResponse

from fair.models import Fair
from accounting.models import (
    Category,
    ChildProduct,
    Order,
    Product,
    RegistrationSection,
)


class RegistrationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationSection
        read_only_fields = ("id", "name", "description", "hide_from_registration")
        fields = read_only_fields


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ("id", "description", "name", "allow_multiple_purchases")
        fields = read_only_fields


class ProductChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = (
            "name",
            "short_name",
            "max_quantity",
            "unit_price",
            "description",
            "category",
            "display_in_product_list",
            "registration_section",
        )
        fields = read_only_fields + ("id",)

    id = serializers.IntegerField()
    category = CategorySerializer(allow_null=True)
    registration_section = RegistrationSectionSerializer()


class ChildProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProduct
        read_only_fields = ("quantity", "child_product")
        fields = read_only_fields

    child_product = ProductChildSerializer()


class ProductSerializer(ProductChildSerializer):
    class Meta(ProductChildSerializer.Meta):
        read_only_fields = ProductChildSerializer.Meta.read_only_fields + (
            "child_products",
        )
        fields = ProductChildSerializer.Meta.fields + read_only_fields

    child_products = ChildProductSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ("id", "unit_price", "comment")
        fields = read_only_fields + ("product", "quantity")

    product = ProductSerializer()

    def validate(self, data):
        try:
            if int(data["quantity"]) < 0:
                raise
        except:
            raise serializers.ValidationError("quantity must be a positive integer")

        try:
            product_id = int(data["product"]["id"])
        except:
            raise serializers.ValidationError("product.id must be a positive integer")

        try:
            if not Product.objects.get(id=product_id):
                raise
        except:
            raise serializers.ValidationError("product does not exist")

        return data

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data["product"]["id"])
        if not product:
            return

        return Order.objects.create(
            product=product,
            quantity=int(validated_data["quantity"]),
            purchasing_company=self.context["purchasing_company"],
        )


def list_products(request):
    user = get_user(request)
    if user == None:
        return JSONError(status.UNAUTHORIZED)

    fair = Fair.objects.get(current=True)
    contact = get_company_contact(user)
    company = contact.company
    contract, signature = get_contract_signature(company, fair, type="INITIAL")

    q = Q(exclusively_for=[])
    if signature == None:
        q |= Q(exclusively_for__contains=["ir-unsigned"])
    else:
        q |= Q(exclusively_for__contains=["ir-signed"])

    products = Product.objects.filter(revenue__fair=fair).filter(q)

    return JsonResponse(ProductSerializer(products, many=True).data, safe=False)
