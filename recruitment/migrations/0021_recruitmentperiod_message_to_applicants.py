# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-17 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recruitment", "0020_merge_20181004_0955"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruitmentperiod",
            name="message_to_applicants",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
