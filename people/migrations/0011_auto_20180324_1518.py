# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_remove_profile_portrait'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('base', 'People'),)},
        ),
    ]
