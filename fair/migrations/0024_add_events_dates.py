# Generated by Django 2.2.24 on 2024-03-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fair", "0023_add_ir_acceptance_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="fair",
            name="events_end_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="fair",
            name="events_start_date",
            field=models.DateTimeField(
                help_text="The date when events will start", null=True
            ),
        ),
    ]
