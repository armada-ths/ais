# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-03 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0007_profile_kth_synchronize"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="drivers_license",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="Driver's license"
            ),
        ),
    ]
