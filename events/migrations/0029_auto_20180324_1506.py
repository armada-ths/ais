# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_eventattendence_sent_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': (('base', 'Events'),)},
        ),
    ]
