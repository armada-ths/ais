# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-28 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banquet", "0011_auto_20181011_1329"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="charge_stripe",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
