# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-08 17:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0045_auto_20171108_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vectorknn',
            name='exhibitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exhibitors.Exhibitor'),
        ),
    ]
