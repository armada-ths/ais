from django.db import models


# A 'Product' is a purchasable item that belongs to a 'Fair'
class Product(models.Model):
    fair = models.ForeignKey('fair.Fair')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    # Chart of accounts number (sv. kontonummer), used for accounting
    coa_number = models.PositiveSmallIntegerField()
    price = models.IntegerField()

    def __str__(self):
        return "%s, %s" % (self.name, self.fair.name)


# An 'Exhibitor' places an 'Order' for a 'Product'
class Order(models.Model):
    exhibitor = models.ForeignKey(
        'exhibitors.Exhibitor', on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    amount = models.PositiveSmallIntegerField()

    def price(self):
        return self.product.price * self.amount

    def __str__(self):
        return "%s order for %s" % (self.exhibitor.company.name, self.product)
