# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0017_auto_20170330_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuisnessArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='sales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.BuisnessArea'),
        ),
    ]
