from django.db import models


class TransportationOrder(models.Model):
    number_of_packages = models.IntegerField(default=0)
    number_of_pallets = models.IntegerField(default=0)
    goods_description = models.TextField(max_length=250, blank=True)
    contact_name = models.CharField(max_length=50, blank=True)
    contact_phone_number = models.CharField(max_length=50, blank=True)

    pickup_street_address = models.CharField(max_length=100, blank=True)
    pickup_zip_code = models.CharField(max_length=10, blank=True)
    pickup_city = models.CharField(max_length=50, blank=True)

    delivery_street_address = models.CharField(max_length=100, blank=True)
    delivery_zip_code = models.CharField(max_length=10, blank=True)
    delivery_city = models.CharField(max_length=50, blank=True)

    ## TODO: Delivery and pickup dates
