# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-29 09:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0021_auto_20180929_0951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exhibitor',
            options={'default_permissions': [], 'permissions': [('base', 'Exhibitors'), ('transport', 'Modify exhibitor transport details')]},
        ),
    ]
