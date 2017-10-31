# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 13:22
from __future__ import unicode_literals

from django.db import migrations, models


def move_tags(apps, schema_editor):
    Product = apps.get_model('orders', 'Product')
    Order = apps.get_model('orders', 'Order')
    Tag = apps.get_model('fair', 'Tag')
    Exhibitor = apps.get_model('exhibitors', 'Exhibitor')

    rooms = Product.objects.filter(product_type__name = ('Rooms'))


    for order in Order.objects.filter(product__in=rooms, amount__gte=1):
        exhibitor = order.exhibitor
        if order.product.name == 'Diversery Room':
            tag = Tag.objects.filter(name='Diversety').first()
            exhibitor.tags.add(tag)
            exhibitor.save()

        if order.product.name == 'Green Room':
            tag = Tag.objects.filter(name='Sustainability').first()
            exhibitor.tags.add(tag)
            exhibitor.save()

class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0065_exhibitor_tags'),
        ('fair', '0006_auto_20170831_2211'),
        ('orders', '0006_auto_20170525_1838'),
    ]

    operations = [
        migrations.RunPython(move_tags),
    ]