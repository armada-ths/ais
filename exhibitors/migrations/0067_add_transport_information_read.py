# Generated by Django 2.2.24 on 2023-08-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibitors", "0066_auto_20210918_2247"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitor",
            name="transport_information_read",
            field=models.BooleanField(default=False),
        ),
    ]
