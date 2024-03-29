# Generated by Django 2.2.24 on 2023-08-16 10:03

import accounting.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0028_add_exclusively_for"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "default_permissions": [],
                "ordering": ["ordering"],
                "permissions": [
                    ("base", "View the Accounting tab"),
                    ("export_orders", "Export orders"),
                    ("ths_customer_ids", "Edit companies without THS customer IDs"),
                ],
                "verbose_name_plural": "Products",
            },
        ),
        migrations.AlterField(
            model_name="product",
            name="exclusively_for",
            field=accounting.models.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("ir-signed", "Companies who have signed IR"),
                        ("ir-unsigned", "Companies who have NOT signed IR"),
                    ],
                    max_length=31,
                ),
                blank=True,
                default=list,
                help_text="Show this product only to the selected company types. An empty selection means showing it to every company.",
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="ordering",
            field=models.IntegerField(
                default=1000,
                help_text="Order the product. The higher the number, the higher the sorting.",
            ),
        ),
    ]
