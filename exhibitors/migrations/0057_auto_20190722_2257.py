# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-22 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0056_auto_20190721_1353"),
    ]

    operations = [
        migrations.CreateModel(
            name="CatalogueCompetence",
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
                ("competence", models.CharField(max_length=255)),
                (
                    "include_in_form",
                    models.BooleanField(
                        default=True,
                        help_text="The alternative is only visible in forms if this attribute is checked.",
                    ),
                ),
            ],
            options={
                "ordering": ["competence"],
                "default_permissions": [],
            },
        ),
        migrations.AlterModelOptions(
            name="cataloguebenefit",
            options={"default_permissions": [], "ordering": ["benefit"]},
        ),
        migrations.AlterModelOptions(
            name="catalogueemployment",
            options={"default_permissions": [], "ordering": ["employment"]},
        ),
        migrations.AlterModelOptions(
            name="catalogueindustry",
            options={"default_permissions": [], "ordering": ["industry"]},
        ),
        migrations.AlterModelOptions(
            name="cataloguelocation",
            options={"default_permissions": [], "ordering": ["location"]},
        ),
        migrations.AlterModelOptions(
            name="cataloguevalue",
            options={"default_permissions": [], "ordering": ["value"]},
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="catalogue_competences",
            field=models.ManyToManyField(
                blank=True, to="exhibitors.CatalogueCompetence"
            ),
        ),
    ]
