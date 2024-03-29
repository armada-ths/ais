# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 13:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lib.image


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0008_alter_user_username_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=75)),
                ("event_start", models.DateTimeField()),
                ("event_end", models.DateTimeField()),
                ("capacity", models.PositiveSmallIntegerField(blank=True, default=0)),
                ("description", models.TextField(blank=True)),
                ("description_short", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=75)),
                (
                    "attendence_description",
                    models.TextField(
                        blank=True,
                        help_text="This is a text only shown in the attendence form, example         'To be accepted to this event you need to pay the event fee of         500 SEK'",
                    ),
                ),
                (
                    "attendence_approvement_required",
                    models.BooleanField(
                        default=True,
                        help_text="If this is checked all users that attends the event needs to         be accepted by an admin.",
                    ),
                ),
                ("external_signup_url", models.URLField(blank=True)),
                ("registration_required", models.BooleanField(default=True)),
                ("registration_start", models.DateTimeField()),
                ("registration_end", models.DateTimeField()),
                (
                    "registration_last_day_cancel",
                    models.DateTimeField(
                        help_text="Last day a user can cancel the attendence to the event",
                        null=True,
                    ),
                ),
                (
                    "public_registration",
                    models.BooleanField(
                        default=False,
                        help_text="If users without an account should be able to sign up for         this event.",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=False,
                        help_text="If the event should be published in the apps and on the website.",
                    ),
                ),
                (
                    "send_submission_mail",
                    models.BooleanField(
                        default=False,
                        help_text="If checked an email will be sent when a user attends         the event",
                    ),
                ),
                (
                    "submission_mail_subject",
                    models.CharField(blank=True, max_length=78),
                ),
                ("submission_mail_body", models.TextField(blank=True)),
                (
                    "confirmation_mail_subject",
                    models.CharField(blank=True, max_length=78),
                ),
                ("confirmation_mail_body", models.TextField(blank=True)),
                ("rejection_mail_subject", models.CharField(blank=True, max_length=78)),
                ("rejection_mail_body", models.TextField(blank=True)),
                (
                    "image_original",
                    models.ImageField(
                        blank=True,
                        upload_to=lib.image.UploadToDirUUID("events", "image_original"),
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to=lib.image.UploadToDir("events", "image")
                    ),
                ),
                (
                    "allowed_groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Choose which groups in armada should be able to see and         attend this event. NOTE: No groups make the event accesible to all         ais-users.",
                        to="auth.Group",
                    ),
                ),
            ],
            options={
                "permissions": (("base", "Events"),),
            },
        ),
        migrations.CreateModel(
            name="EventAnswer",
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
                ("answer", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="EventAttendence",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "Approved"),
                            ("C", "Canceled"),
                            ("D", "Declined"),
                            ("S", "Submitted"),
                        ],
                        default="S",
                        max_length=3,
                    ),
                ),
                (
                    "submission_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("sent_email", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.Event"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventQuestion",
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
                ("question_text", models.TextField()),
                ("required", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.Event"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="eventanswer",
            name="attendence",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="events.EventAttendence"
            ),
        ),
        migrations.AddField(
            model_name="eventanswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="events.EventQuestion"
            ),
        ),
    ]
