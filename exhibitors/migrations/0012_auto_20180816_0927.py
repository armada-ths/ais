# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0011_auto_20180814_1504"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitor",
            name="catalogue_about",
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name="exhibitor",
            name="catalogue_purpose",
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
    ]
