# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-17 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fair", "0010_auto_20181111_1830"),
    ]

    operations = [
        migrations.AddField(
            model_name="lunchticket",
            name="sent",
            field=models.BooleanField(default=False),
        ),
    ]
