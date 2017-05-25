from django.db import models


# A 'Product' is a purchasable item that belongs to a 'Fair'
class Product(models.Model):
    fair = models.ForeignKey('fair.Fair')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    # Chart of accounts number (sv. kontonummer), used for accounting
    coa_number = models.PositiveSmallIntegerField()
    price = models.IntegerField()

    class Meta:
        ordering = ['name']
        permissions = (('view_products', 'View products'),)

	#The orders that come from accepted exhibitors
    def confirmed_quantity(self):
        return sum([order.amount * order.is_confirmed() for order in self.order_set.all()])

    def ordered_quantity(self):
        return sum([order.amount for order in self.order_set.all()])

    def confirmed_revenue(self):
        return self.confirmed_quantity() * self.price

    def revenue(self):
        return self.ordered_quantity() * self.price

    def __str__(self):
        return "%s, %s" % (self.name, self.fair.name)


# An 'Exhibitor' places an 'Order' for a 'Product'
class Order(models.Model):
    exhibitor = models.ForeignKey(
        'exhibitors.Exhibitor', on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["product"]

    def is_confirmed(self):
        return self.exhibitor.status == 'accepted'

    def price(self):
        return self.product.price * self.amount

    def __str__(self):
        return "%s order for %s" % (self.exhibitor.company.name, self.product)
