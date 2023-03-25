# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-22 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0018_lunchticket_email_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lunchticket",
            name="email_address",
            field=models.EmailField(max_length=255, verbose_name="E-mail address"),
        ),
    ]
