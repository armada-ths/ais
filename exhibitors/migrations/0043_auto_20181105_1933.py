# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-05 18:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fair", "0004_auto_20181003_1227"),
        ("exhibitors", "0042_remove_lunchticket_exhibitor"),
    ]

    operations = [
        migrations.CreateModel(
            name="LunchTicketTime",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "fair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="fair.Fair"
                    ),
                ),
            ],
            options={
                "ordering": ["fair", "name"],
                "default_permissions": [],
            },
        ),
        migrations.AddField(
            model_name="lunchticket",
            name="time",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="exhibitors.LunchTicketTime",
            ),
        ),
    ]
