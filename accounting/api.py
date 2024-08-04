from rest_framework import serializers

from accounting.models import (
    Category,
    ChildProduct,
    Order,
    Product,
    RegistrationSection,
    SpecificProduct,
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


def get_product_orders(product):
    return Order.objects.filter(
        product__id=product.id, purchasing_company__signature__contract__type="COMPLETE"
    )


class ProductChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = (
            "name",
            "short_name",
            "max_quantity",
            "out_of_stock",
            "unit_price",
            "description",
            "category",
            "display_in_product_list",
            "registration_section",
        )
        fields = read_only_fields + ("id",)

    id = serializers.IntegerField()
    out_of_stock = serializers.SerializerMethodField()
    category = CategorySerializer(allow_null=True)
    registration_section = RegistrationSectionSerializer()

    def get_out_of_stock(self, obj):
        stock = obj.stock
        if stock == None:
            return None

        orders = get_product_orders(obj)
        amount_ordered = sum([order.quantity for order in orders])

        return amount_ordered >= stock.amount


class ChildProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProduct
        read_only_fields = ("quantity", "child_product")
        fields = read_only_fields

    child_product = ProductChildSerializer()


class SpecificProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificProduct
        read_only_fields = ("unit_price", "specific_product")
        fields = read_only_fields

    specific_product = ProductChildSerializer()


class ProductSerializer(ProductChildSerializer):
    class Meta(ProductChildSerializer.Meta):
        read_only_fields = ProductChildSerializer.Meta.read_only_fields + (
            "child_products",
            "specific_products",
        )
        fields = ProductChildSerializer.Meta.fields + read_only_fields

    child_products = ChildProductSerializer(many=True)
    specific_products = SpecificProductSerializer(many=True)


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

        stock_when_bought = None
        if product.stock != None:
            orders = get_product_orders(product)
            amount_ordered = sum([order.quantity for order in orders])
            stock_when_bought = amount_ordered - product.stock.amount

        return Order.objects.create(
            product=product,
            quantity=int(validated_data["quantity"]),
            purchasing_company=self.context["purchasing_company"],
            stock_when_bought=stock_when_bought,
        )
