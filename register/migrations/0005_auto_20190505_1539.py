# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-05 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0004_signupcontract_default"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupcontract",
            name="current",
            field=models.BooleanField(
                default=True,
                help_text="Used to determine which contract for a fair, type and company type that should be used if several have been uploaded. Only one contract in this group can be marked as current.",
            ),
        ),
        migrations.AlterField(
            model_name="signupcontract",
            name="default",
            field=models.BooleanField(
                default=False,
                help_text="Used to determine which contract for a fair and type that is the default one. Only one contract per fair and type can be marked as current, <strong>make sure one default contract exists before registration opens.</strong>.",
            ),
        ),
    ]
