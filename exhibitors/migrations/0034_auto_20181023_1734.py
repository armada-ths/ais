# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-23 15:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0033_exhibitor_deadline_complete_registration"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exhibitor",
            options={
                "default_permissions": [],
                "permissions": [
                    ("base", "View the Exhibitors tab"),
                    ("view_all", "Always view all exhibitors"),
                    ("create", "Create new exhibitors"),
                    ("modify_contact_persons", "Modify contact persons"),
                    ("modify_transport", "Modify transport details"),
                    ("modify_details", "Modify details"),
                ],
            },
        ),
    ]
