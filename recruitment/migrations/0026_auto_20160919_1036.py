# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0025_auto_20160911_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roleapplication',
            options={'ordering': ['order']},
        ),
    ]
