# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-22 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0027_company_e_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='e_invoice',
            field=models.BooleanField(default=False, help_text='This attribute should be checked if the company uses e-invoices'),
        ),
    ]
