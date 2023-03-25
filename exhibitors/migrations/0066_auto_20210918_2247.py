# Generated by Django 2.2.24 on 2021-09-18 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitors", "0065_auto_20200929_0214"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitor",
            name="check_in_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="check_in_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="exhibitor",
            name="fair_location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="exhibitors.Location",
            ),
        ),
    ]
