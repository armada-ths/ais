# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-27 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0059_auto_20190727_1215"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cataloguecategory",
            options={
                "default_permissions": [],
                "ordering": ["category"],
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="catalogueindustry",
            options={
                "default_permissions": [],
                "ordering": ["category", "industry"],
                "verbose_name_plural": "Industries",
            },
        ),
    ]
