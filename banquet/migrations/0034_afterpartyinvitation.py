# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-12 17:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("banquet", "0033_participant_has_paid"),
    ]

    operations = [
        migrations.CreateModel(
            name="AfterPartyInvitation",
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
                ("name", models.CharField(max_length=75, verbose_name="Full name")),
                (
                    "email_address",
                    models.EmailField(
                        max_length=75, unique=True, verbose_name="E-mail address"
                    ),
                ),
                ("used", models.BooleanField(default=False)),
                (
                    "banquet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="banquet.Banquet",
                    ),
                ),
                (
                    "inviter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
