# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-04 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("people", "0011_auto_20181107_1416"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="other_dietary_restrictions",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]
