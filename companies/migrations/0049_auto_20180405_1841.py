# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-05 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0048_auto_20180404_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycustomerresponsible',
            name='group',
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='groups',
            field=models.ManyToManyField(to='companies.Group'),
        ),
    ]