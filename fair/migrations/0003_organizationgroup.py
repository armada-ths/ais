# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-03 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fair", "0002_fair_product_lunch_ticket"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationGroup",
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
        ),
    ]
