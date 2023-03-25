# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-28 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0012_participant_charge_stripe"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvitationGroup",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("deadline", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="invitation",
            name="token",
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]
