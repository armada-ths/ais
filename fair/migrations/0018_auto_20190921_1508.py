# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-21 15:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0017_lunchticket_dietary_restrictions_other'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lunchticket',
            old_name='dietary_restrictions_other',
            new_name='other_dietary_restrictions',
        ),
    ]