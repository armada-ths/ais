# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-01 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0032_merge_20190925_2233"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="has_paid",
            field=models.BooleanField(default=False),
        ),
    ]
