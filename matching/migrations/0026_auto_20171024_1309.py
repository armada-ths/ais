# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0025_auto_20171024_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continent',
            name='continent',
            field=models.TextField(unique=True),
        ),
    ]
