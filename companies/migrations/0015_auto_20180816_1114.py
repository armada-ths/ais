# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0014_auto_20180816_1106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Organization name"
            ),
        ),
        migrations.AlterField(
            model_name="companyaddress",
            name="name",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Name, if different from the organization name",
            ),
        ),
    ]
