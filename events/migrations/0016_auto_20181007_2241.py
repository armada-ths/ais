# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-07 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0015_checkintoken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkintoken",
            name="check_in_timestamp",
            field=models.DateTimeField(
                null=True, verbose_name="When the token was last used to check in"
            ),
        ),
    ]
