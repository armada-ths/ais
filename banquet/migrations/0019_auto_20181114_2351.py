# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-14 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0018_auto_20181114_2346"),
    ]

    operations = [
        migrations.AlterField(
            model_name="afterpartyticket",
            name="email_address",
            field=models.EmailField(
                blank=True, max_length=75, null=True, verbose_name="E-mail address"
            ),
        ),
    ]
