# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0025_auto_20181118_1911"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="attended",
            field=models.BooleanField(default=False),
        ),
    ]
