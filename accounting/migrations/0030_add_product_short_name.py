# Generated by Django 2.2.24 on 2023-08-16 10:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0029_remove_category_ordering"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="short_name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
