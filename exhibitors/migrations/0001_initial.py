# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 13:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lib.image


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("transportation", "0001_initial"),
        ("locations", "0001_initial"),
        ("companies", "0002_auto_20180730_1515"),
        ("fair", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CatalogInfo",
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
                ("display_name", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, db_index=False)),
                ("short_description", models.CharField(blank=True, max_length=200)),
                ("description", models.TextField()),
                ("employees_sweden", models.IntegerField(default=0)),
                ("employees_world", models.IntegerField(default=0)),
                ("countries", models.IntegerField(default=0)),
                ("website_url", models.CharField(blank=True, max_length=300)),
                ("facebook_url", models.CharField(blank=True, max_length=300)),
                ("twitter_url", models.CharField(blank=True, max_length=300)),
                ("linkedin_url", models.CharField(blank=True, max_length=300)),
                (
                    "logo_original",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID(
                            "exhibitors", "logo_original"
                        ),
                    ),
                ),
                (
                    "logo_small",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDir("exhibitors", "logo_small"),
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDir("exhibitors", "logo"),
                    ),
                ),
                (
                    "ad_original",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID(
                            "exhibitors", "ad_original"
                        ),
                    ),
                ),
                (
                    "ad",
                    models.ImageField(
                        blank=True, upload_to=lib.image.UploadToDir("exhibitors", "ad")
                    ),
                ),
                (
                    "location_at_fair_original",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID(
                            "exhibitors", "location_at_fair_original"
                        ),
                    ),
                ),
                (
                    "location_at_fair",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDir(
                            "exhibitors", "location_at_fair"
                        ),
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Continent",
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
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="Exhibitor",
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
                ("booth_number", models.IntegerField(blank=True, null=True)),
                ("about_text", models.TextField(blank=True)),
                ("facts_text", models.TextField(blank=True)),
                ("accept_terms", models.BooleanField(default=False)),
                ("comment", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("accepted", "Accepted"),
                            ("registered", "Registered"),
                            ("complete_registration", "Completed Registration"),
                            ("complete_registration_submit", "CR - Submitted"),
                            ("complete_registration_start", "CR - In Progress"),
                            ("complete_registration_terms", "CR - Accepted Terms"),
                            ("contacted_by_host", "Contacted by host"),
                            ("confirmed", "Confirmed"),
                            ("checked_in", "Checked in"),
                            ("checked_out", "Checked out"),
                            ("withdrawn", "Withdrawn"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID(
                            "exhibitors", "logo_original"
                        ),
                    ),
                ),
                (
                    "location_at_fair",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID(
                            "exhibitors", "location_at_fair"
                        ),
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.Company",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.CompanyContact",
                    ),
                ),
                (
                    "delivery_order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="delivery_order",
                        to="transportation.TransportationOrder",
                    ),
                ),
                (
                    "fair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="fair.Fair"
                    ),
                ),
            ],
            options={
                "permissions": (("base", "Exhibitors"),),
            },
        ),
        migrations.CreateModel(
            name="ExhibitorView",
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
                ("choices", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobType",
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
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="TransportationAlternative",
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
                ("name", models.CharField(max_length=150)),
                (
                    "transportation_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("3rd_party", "Third party"),
                            ("self", "By Customer"),
                            ("internal", "Fair arranger"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                ("inbound", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Value",
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
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="WorkField",
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
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="fair_location",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="locations.Location",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="hosts",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="inbound_transportation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="inbound_transportation",
                to="exhibitors.TransportationAlternative",
                verbose_name="Transportation to the fair",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="job_types",
            field=models.ManyToManyField(blank=True, to="exhibitors.JobType"),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="exhibitors.Location",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="outbound_transportation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="outbound_transportation",
                to="exhibitors.TransportationAlternative",
                verbose_name="Transportation from the fair",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="pickup_order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pickup_order",
                to="transportation.TransportationOrder",
            ),
        ),
        migrations.AddField(
            model_name="exhibitor",
            name="tags",
            field=models.ManyToManyField(blank=True, to="fair.Tag"),
        ),
        migrations.AddField(
            model_name="cataloginfo",
            name="continents",
            field=models.ManyToManyField(blank=True, to="exhibitors.Continent"),
        ),
        migrations.AddField(
            model_name="cataloginfo",
            name="exhibitor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="exhibitors.Exhibitor"
            ),
        ),
        migrations.AddField(
            model_name="cataloginfo",
            name="job_types",
            field=models.ManyToManyField(blank=True, to="exhibitors.JobType"),
        ),
        migrations.AddField(
            model_name="cataloginfo",
            name="main_work_field",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="exhibitors.WorkField",
            ),
        ),
    ]
