# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-14 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0016_auto_20181028_1429"),
    ]

    operations = [
        migrations.CreateModel(
            name="AfterPartyTicket",
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
                    "token",
                    models.CharField(default=uuid.uuid4, max_length=255, unique=True),
                ),
                ("name", models.CharField(blank=True, max_length=75, null=True)),
                (
                    "email_address",
                    models.CharField(blank=True, max_length=75, null=True),
                ),
                ("paid_timestamp", models.DateTimeField(auto_now_add=True)),
                ("paid_price", models.PositiveIntegerField()),
            ],
        ),
    ]
