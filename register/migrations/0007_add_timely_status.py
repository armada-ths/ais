# Generated by Django 2.2.24 on 2024-08-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0006_add_signup_log_ip"),
    ]

    operations = [
        migrations.AddField(
            model_name="signupcontract",
            name="is_timely",
            field=models.BooleanField(
                default=True,
                help_text="(ONLY RELEVANT FOR IR) A contract is timely if it is signed before the IR period ends.",
            ),
        ),
    ]
