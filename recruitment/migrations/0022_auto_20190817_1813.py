# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-17 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0021_recruitmentperiod_message_to_applicants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentperiod',
            name='message_to_applicants',
            field=models.TextField(blank=True, null=True),
        ),
    ]
