# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-22 14:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fair", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exhibitors", "0015_auto_20180922_1635"),
    ]

    operations = [
        migrations.CreateModel(
            name="LunchTicket",
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
                ("comment", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="LunchTicketDay",
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
            options={
                "ordering": ["fair", "name"],
            },
        ),
        migrations.CreateModel(
            name="LunchTicketScan",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "lunch_ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exhibitors.LunchTicket",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="about_text",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="accept_terms",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="booth_number",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="facts_text",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="fair_location",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="job_types",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="location",
        ),
        migrations.RemoveField(
            model_name="exhibitor",
            name="tags",
        ),
        migrations.DeleteModel(
            name="JobType",
        ),
        migrations.DeleteModel(
            name="Location",
        ),
        migrations.AddField(
            model_name="lunchticket",
            name="day",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="exhibitors.LunchTicketDay",
            ),
        ),
        migrations.AddField(
            model_name="lunchticket",
            name="exhibitor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="exhibitors.Exhibitor"
            ),
        ),
    ]
