# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0018_auto_20181009_1144"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="check_in_token",
            field=models.CharField(
                default="48jf2JfsKwGOn5rPYLaXkhkYE8seqo2w", max_length=32, unique=True
            ),
        ),
    ]
