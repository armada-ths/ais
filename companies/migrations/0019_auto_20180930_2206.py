# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-30 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0018_companycustomercomment_show_in_exhibitors"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="companycontact",
            options={"ordering": ["-active", "first_name"]},
        ),
    ]
