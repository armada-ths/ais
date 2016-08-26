# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-26 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0008_auto_20160822_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='AISPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('codename', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(to='recruitment.AISPermission'),
        ),
    ]
