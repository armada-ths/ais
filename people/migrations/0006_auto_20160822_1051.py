# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 10:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20160820_2101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programme',
            options={'ordering': ['name']},
        ),
    ]
