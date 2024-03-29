# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-29 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("unirel", "0007_auto_20181029_1252"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="unirel_participant_company",
                to="companies.Company",
                verbose_name="Organization",
            ),
        ),
    ]
