# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-28 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0018_auto_20190727_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationsection',
            name='include_in_registration',
            field=models.BooleanField(default=True, help_text='The section is only visible in the registration if this attribute is checked.'),
        ),
    ]