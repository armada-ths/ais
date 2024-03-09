# Generated by Django 2.2.24 on 2024-03-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0031_remove_countries_choice"),
    ]

    operations = [
        migrations.AddField(
            model_name="companytype",
            name="default",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="companycontact",
            name="confirmed",
            field=models.BooleanField(
                default=False,
                verbose_name="This contact has been confirmed to be a real contact in the company",
            ),
        ),
    ]
