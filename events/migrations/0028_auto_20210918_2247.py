# Generated by Django 2.2.24 on 2021-09-18 22:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0027_participant_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupquestion",
            name="options",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(), default=list, size=None
            ),
        ),
    ]
