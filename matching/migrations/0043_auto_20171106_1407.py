# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-06 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0071_auto_20171030_2040'),
        ('matching', '0042_auto_20171106_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtype',
            name='exhibitors',
            field=models.ManyToManyField(blank=True, to='exhibitors.Exhibitor'),
        ),
        migrations.AlterField(
            model_name='country',
            name='exhibitor',
            field=models.ManyToManyField(blank=True, to='exhibitors.Exhibitor'),
        ),
        migrations.AlterField(
            model_name='swedencity',
            name='exhibitor',
            field=models.ManyToManyField(blank=True, to='exhibitors.Exhibitor'),
        ),
        migrations.AlterField(
            model_name='swedencity',
            name='region',
            field=models.ManyToManyField(blank=True, to='matching.SwedenRegion'),
        ),
        migrations.AlterField(
            model_name='swedenregion',
            name='exhibitors',
            field=models.ManyToManyField(blank=True, to='exhibitors.Exhibitor'),
        ),
        migrations.AlterField(
            model_name='workfield',
            name='exhibitors',
            field=models.ManyToManyField(blank=True, to='exhibitors.Exhibitor'),
        ),
    ]
