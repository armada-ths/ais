# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0005_auto_20160808_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfield',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customfieldargument',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
