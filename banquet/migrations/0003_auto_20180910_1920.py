# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-10 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banquet', '0002_auto_20180730_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banquet',
            name='fair',
        ),
        migrations.RemoveField(
            model_name='banquettable',
            name='fair',
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='exhibitor',
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='fair',
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='table',
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='banquetteattendant',
            name='user',
        ),
        migrations.DeleteModel(
            name='Banquet',
        ),
        migrations.DeleteModel(
            name='BanquetTable',
        ),
        migrations.DeleteModel(
            name='BanquetteAttendant',
        ),
        migrations.DeleteModel(
            name='BanquetTicket',
        ),
    ]