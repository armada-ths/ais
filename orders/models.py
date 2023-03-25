from django.db import models


class ProductType(models.Model):
    """
    A 'ProductType' is a type that seperates a different kidns of products
    Some of the frontend can present products grouped by types.
    The description can also be added to display a longer description text about
    the product type.
    """

    name = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    policies = (
        ("SELECT", "Select one"),
        ("SELECT_MULTIPLE", "Select multipe"),
        ("SELECT_MULTIPLE_Amount", "Select multipe with amount"),
    )
    selection_policy = models.CharField(
        choices=policies, default="SELECT", max_length=25
    )

    # Variable for control of what products are visible to exhibitors in their registration
    display_in_product_list = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "%s" % self.name


class Product(models.Model):
    """
    A 'Product' is a purchasable item that belongs to a 'Fair' and has a 'ProductType'
    """

    fair = models.ForeignKey("fair.Fair", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    # Chart of accounts number (sv. kontonummer), used for accounting
    coa_number = models.PositiveSmallIntegerField()
    price = models.IntegerField()
    product_type = models.ForeignKey(
        ProductType, null=True, blank=True, on_delete=models.CASCADE
    )

    # Variable for control of what products are visible to exhibitors in their registration
    display_in_product_list = models.BooleanField(default=True)

    included_for_all = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        permissions = (("base", "Products"),)

    def ordered_quantity(self):
        return sum([order.amount for order in self.order_set.all()])

    def revenue(self):
        return self.ordered_quantity() * self.price

    def __str__(self):
        return "%s - %s, %s, %i :-" % (
            self.product_type,
            self.name,
            self.fair.name,
            self.price,
        )


class StandArea(Product):
    width = models.IntegerField()
    depth = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return "%s, %i x %i x %i,  %s, + %i :-" % (
            self.name,
            self.width,
            self.depth,
            self.height,
            self.fair.name,
            self.price,
        )


class Order(models.Model):
    """
    An 'Exhibitor' places an 'Order' for a 'Product'
    """

    exhibitor = models.ForeignKey("exhibitors.Exhibitor", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["product"]

    def price(self):
        return self.product.price * self.amount

    def __str__(self):
        return "%s order for %s" % (self.exhibitor.company.name, self.product)


class ElectricityOrder(models.Model):
    exhibitor = models.ForeignKey("exhibitors.Exhibitor", on_delete=models.CASCADE)
    total_power = models.IntegerField(default=0)
    number_of_outlets = models.IntegerField(default=0)
    equipment_description = models.CharField(max_length=150, null=True, blank=True)
