# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0055_auto_20170629_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='accept_terms',
            field=models.BooleanField(default=False),
        ),
    ]
