# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0007_auto_20161010_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cataloginfo',
            name='display_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='cataloginfo',
            name='short_description',
            field=models.CharField(max_length=200),
        ),
    ]
