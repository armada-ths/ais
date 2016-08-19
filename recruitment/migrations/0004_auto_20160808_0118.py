# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_recruitmentapplication_exhibitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentapplication',
            name='status',
            field=models.CharField(blank=True, choices=[('undecided', 'Undecided'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=20, null=True),
        ),
    ]
