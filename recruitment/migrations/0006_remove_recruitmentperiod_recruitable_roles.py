# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-28 10:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recruitment", "0005_auto_20180819_1437"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recruitmentperiod",
            name="recruitable_roles",
        ),
    ]
