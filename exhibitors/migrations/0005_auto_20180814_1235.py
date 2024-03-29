# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-14 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0004_auto_20180806_0219"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitor",
            name="placement_comment",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Additional wishes regarding placement at the fair",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="placement_wish",
            field=models.CharField(
                blank=True,
                choices=[
                    ("accepted", "No wish"),
                    ("MIXED", "Mixed with companies from other industries"),
                    ("SIMILAR", "Next to similar companies"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
