# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-08 08:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0079_auto_20180708_1040'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='companycustomerresponsible',
            unique_together=set([('company', 'group')]),
        ),
        migrations.RemoveField(
            model_name='companycustomercomment',
            name='company_customer',
        ),
        migrations.AlterField(
            model_name='companycustomercomment',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AlterField(
            model_name='companycustomerresponsible',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.RemoveField(
            model_name='companycustomerresponsible',
            name='company_customer',
        ),
    ]
