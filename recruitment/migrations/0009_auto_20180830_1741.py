# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recruitment", "0008_auto_20180830_1739"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recruitmentapplication",
            name="interview_date",
        ),
        migrations.RemoveField(
            model_name="recruitmentapplication",
            name="interview_location",
        ),
        migrations.AddField(
            model_name="recruitmentapplication",
            name="slot",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="recruitment.Slot",
            ),
        ),
    ]
