# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-11 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0009_auto_20181111_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lunchticket',
            name='time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fair.LunchTicketTime'),
        ),
    ]
