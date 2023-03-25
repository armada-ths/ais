# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Banquet",
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
            ],
            options={
                "permissions": (("base", "Banquet"),),
            },
        ),
        migrations.CreateModel(
            name="BanquetTable",
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
                ("table_name", models.CharField(blank=True, max_length=60, null=True)),
                ("number_of_seats", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "ordering": ["table_name"],
            },
        ),
        migrations.CreateModel(
            name="BanquetteAttendant",
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
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("phone_number", models.CharField(max_length=200)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                            ("not_specify", "Prefer not to specify"),
                        ],
                        max_length=100,
                    ),
                ),
                ("job_title", models.CharField(blank=True, max_length=200)),
                ("linkedin_url", models.URLField(blank=True)),
                ("allergies", models.CharField(blank=True, max_length=1000)),
                ("wants_alcohol", models.BooleanField(default=True)),
                ("wants_lactose_free_food", models.BooleanField(default=False)),
                ("wants_gluten_free_food", models.BooleanField(default=False)),
                ("wants_vegan_food", models.BooleanField(default=False)),
                ("seat_number", models.SmallIntegerField(blank=True, null=True)),
                ("student_ticket", models.BooleanField(default=False)),
                ("confirmed", models.BooleanField(default=False)),
                ("ignore_from_placement", models.BooleanField(default=False)),
            ],
            options={
                "permissions": (("can_seat_attendants", "Can seat attendants"),),
                "ordering": ["first_name", "last_name"],
            },
        ),
        migrations.CreateModel(
            name="BanquetTicket",
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
                ("name", models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
