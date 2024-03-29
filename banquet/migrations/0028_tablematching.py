# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-19 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0061_auto_20190727_1229"),
        ("banquet", "0027_auto_20181119_2258"),
    ]

    operations = [
        migrations.CreateModel(
            name="TableMatching",
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
                (
                    "catalogue_competences",
                    models.ManyToManyField(
                        blank=True, to="exhibitors.CatalogueCompetence"
                    ),
                ),
                (
                    "catalogue_employments",
                    models.ManyToManyField(
                        blank=True, to="exhibitors.CatalogueEmployment"
                    ),
                ),
                (
                    "catalogue_industries",
                    models.ManyToManyField(
                        blank=True, to="exhibitors.CatalogueIndustry"
                    ),
                ),
                (
                    "catalogue_locations",
                    models.ManyToManyField(
                        blank=True, to="exhibitors.CatalogueLocation"
                    ),
                ),
                (
                    "catalogue_values",
                    models.ManyToManyField(blank=True, to="exhibitors.CatalogueValue"),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="banquet.Participant",
                    ),
                ),
            ],
        ),
    ]
