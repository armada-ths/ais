from django.db import models

# A 'ProductType' is a type that seperates a different kidns of products
class ProductType(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=64, null=True, blank=True)

    # The views is information around how these type of products
    # should be shown in forms

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "%s" % self.name

# A 'Product' is a purchasable item that belongs to a 'Fair' and has a 'ProductType'
class Product(models.Model):
    fair = models.ForeignKey('fair.Fair', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    # Chart of accounts number (sv. kontonummer), used for accounting
    coa_number = models.PositiveSmallIntegerField()
    price = models.IntegerField()
    product_type = models.ForeignKey(ProductType, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        permissions = (('view_products', 'View products'),)

    def ordered_quantity(self):
        return sum([order.amount for order in self.order_set.all()])

    def revenue(self):
        return self.ordered_quantity() * self.price

    def __str__(self):
        return "%s, %s" % (self.name, self.fair.name)

class StandArea(Product):
    width = models.IntegerField()
    depth = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return "%s, %i x %i x %i,  %s, + %i :-" % (self.name, self.width, self.depth, self.height,  self.fair.name, self.price)


# An 'Exhibitor' places an 'Order' for a 'Product'
class Order(models.Model):
    exhibitor = models.ForeignKey(
        'exhibitors.Exhibitor', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["product"]

    def price(self):
        return self.product.price * self.amount

    def __str__(self):
        return "%s order for %s" % (self.exhibitor.company.name, self.product)
