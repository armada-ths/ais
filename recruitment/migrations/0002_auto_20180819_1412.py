# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-19 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="role",
            options={
                "ordering": ["recruitment_period", "name"],
                "permissions": (("administer_roles", "Administer roles"),),
            },
        ),
        migrations.AddField(
            model_name="role",
            name="recruitment_period",
            field=models.ForeignKey(
                default=12,
                on_delete=django.db.models.deletion.CASCADE,
                to="recruitment.RecruitmentPeriod",
            ),
            preserve_default=False,
        ),
    ]
