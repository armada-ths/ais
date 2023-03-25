# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("events", "0001_initial"),
        ("recruitment", "0001_initial"),
        ("fair", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="extra_field",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="recruitment.ExtraField",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="fair",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="fair.Fair"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="tags",
            field=models.ManyToManyField(blank=True, to="fair.Tag"),
        ),
    ]
