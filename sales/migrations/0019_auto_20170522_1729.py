# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_auto_20170522_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='sales',
            new_name='buisness_area',
        ),
    ]
