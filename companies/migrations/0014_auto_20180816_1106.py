# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0013_auto_20180816_0910"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="ths_customer_id",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="THS customer ID"
            ),
        ),
    ]
