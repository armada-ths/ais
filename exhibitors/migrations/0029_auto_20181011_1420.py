# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitors", "0028_auto_20181011_1417"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExhibitorInBooth",
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
                ("comment", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "booth",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exhibitors.Booth",
                    ),
                ),
                (
                    "exhibitor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exhibitors.Exhibitor",
                    ),
                ),
            ],
            options={
                "ordering": ["exhibitor", "booth"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="exhibitorinbooth",
            unique_together=set([("exhibitor", "booth")]),
        ),
    ]
