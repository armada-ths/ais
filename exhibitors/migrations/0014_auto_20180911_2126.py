# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitors", "0013_auto_20180911_2116"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exhibitor",
            options={
                "permissions": [
                    ("base", "Exhibitors"),
                    ("transport", "Modify exhibitor transport details"),
                ]
            },
        ),
    ]
