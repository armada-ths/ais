# Generated by Django 2.2.24 on 2023-10-18 10:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0069_map_coordinates"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exhibitor",
            options={
                "default_permissions": [],
                "ordering": ["company__name"],
                "permissions": [
                    ("base", "View the Exhibitors tab"),
                    ("view_all", "Always view all exhibitors"),
                    ("create", "Create new exhibitors"),
                    ("modify_contact_persons", "Modify contact persons"),
                    ("modify_transport", "Modify transport details"),
                    ("modify_check_in", "Modify check in"),
                    ("modify_details", "Modify details"),
                    ("modify_booths", "Modify booths"),
                    ("people_count", "Count people in locations"),
                    ("modify_coordinates", "Modify coordinates"),
                    ("modify_fair_location", "Modify Fair Location"),
                ],
            },
        ),
    ]
