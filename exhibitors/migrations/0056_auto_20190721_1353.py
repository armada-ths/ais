# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-21 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitors", "0055_auto_20190721_0730"),
    ]

    operations = [
        migrations.AddField(
            model_name="cataloguebenefit",
            name="include_in_form",
            field=models.BooleanField(
                default=True,
                help_text="The alternative is only visible in forms if this attribute is checked.",
            ),
        ),
        migrations.AlterField(
            model_name="catalogueemployment",
            name="include_in_form",
            field=models.BooleanField(
                default=True,
                help_text="The alternative is only visible in forms if this attribute is checked.",
            ),
        ),
        migrations.AlterField(
            model_name="catalogueindustry",
            name="include_in_form",
            field=models.BooleanField(
                default=True,
                help_text="The alternative is only visible in forms if this attribute is checked.",
            ),
        ),
        migrations.AlterField(
            model_name="cataloguelocation",
            name="include_in_form",
            field=models.BooleanField(
                default=True,
                help_text="The alternative is only visible in forms if this attribute is checked.",
            ),
        ),
        migrations.AlterField(
            model_name="cataloguevalue",
            name="include_in_form",
            field=models.BooleanField(
                default=True,
                help_text="The alternative is only visible in forms if this attribute is checked.",
            ),
        ),
    ]
