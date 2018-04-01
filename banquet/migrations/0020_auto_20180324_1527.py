# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0008_auto_20180110_1850'),
        ('banquet', '0019_auto_20180324_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banquet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fair', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
            options={
                'permissions': (('base', 'Banquet'),),
            },
        ),
        migrations.AlterModelOptions(
            name='banquetteattendant',
            options={'ordering': ['first_name', 'last_name'], 'permissions': (('can_seat_attendants', 'Can seat attendants'),)},
        ),
    ]