# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-19 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0037_auto_20180119_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='survey',
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='matching.Survey'),
        ),
    ]
