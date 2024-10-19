# Generated by Django 2.2.24 on 2024-09-10 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0014_add_dietary_preferences"),
        ("banquet", "0047_has_sent_mail"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="dietary_preference",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="people.DietaryPreference",
            ),
        ),
    ]
