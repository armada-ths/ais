# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_sale_contact_by_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'permissions': (('base', 'Sales'),)},
        ),
    ]