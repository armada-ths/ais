# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0008_auto_20161010_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitor',
            name='invoice_address_zip_code',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
