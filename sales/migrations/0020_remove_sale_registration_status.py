# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 18:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_sale_registration_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='registration_status',
        ),
    ]
