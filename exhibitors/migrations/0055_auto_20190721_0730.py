# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-21 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0054_auto_20181120_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogueemployment',
            name='include_in_form',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='catalogueindustry',
            name='include_in_form',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cataloguelocation',
            name='include_in_form',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cataloguevalue',
            name='include_in_form',
            field=models.BooleanField(default=True),
        ),
    ]
