# Generated by Django 2.2.24 on 2024-08-04 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0037_add_product_help_texts"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="display_only_when_specific_for_packages",
            field=models.BooleanField(
                default=False,
                help_text="This product will only be shown to the customer if they select a package that has this product as a specific product. When to use this: e.g. A package is gatekeeping this product, only show the product when the package is selected. When not to use this: e.g. This product's price is only affected by one or more packages, but the product is still available for purchase without the package.",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="specific_products",
            field=models.ManyToManyField(
                blank=True,
                help_text='(ONLY RELEVANT FOR PACKAGES AS ROOT PRODUCTS) These products will only be shown to the customer if they select the current package This feature was used in 2024 when silver and bronze packages lead to different prices on the same products Neccessary is to toggle the "Display in product list" to false on for the specific product (otherwise it will be displayed with standard price).',
                to="accounting.SpecificProduct",
            ),
        ),
    ]
