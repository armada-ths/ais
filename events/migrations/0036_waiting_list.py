# Generated by Django 2.2.24 on 2024-11-07 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_merge_20241008_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='in_waiting_list',
            field=models.BooleanField(default=False),
        ),
    ]
