# Generated by Django 2.2.24 on 2023-04-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banquet", "0045_auto_20210918_2247"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banquet",
            name="afterparty_price",
            field=models.PositiveIntegerField(
                default=0, verbose_name="After Party Price (SEK)"
            ),
        ),
        migrations.AlterField(
            model_name="banquet",
            name="afterparty_price_discount",
            field=models.PositiveIntegerField(
                default=0, verbose_name="After Party Discounted Price (SEK)"
            ),
        ),
    ]