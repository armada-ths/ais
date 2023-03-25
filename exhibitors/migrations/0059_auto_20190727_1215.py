# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-27 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitors", "0058_exhibitor_catalogue_cities"),
    ]

    operations = [
        migrations.CreateModel(
            name="CatalogueCategory",
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
                ("category", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ["category"],
                "default_permissions": [],
            },
        ),
        migrations.AlterModelOptions(
            name="cataloguecompetence",
            options={"default_permissions": [], "ordering": ["category", "competence"]},
        ),
        migrations.AlterModelOptions(
            name="catalogueindustry",
            options={"default_permissions": [], "ordering": ["category", "industry"]},
        ),
        migrations.AddField(
            model_name="cataloguecompetence",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="exhibitors.CatalogueCategory",
            ),
        ),
        migrations.AddField(
            model_name="catalogueindustry",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="exhibitors.CatalogueCategory",
            ),
        ),
    ]
