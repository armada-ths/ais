# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-19 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fair', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('organisation_number', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('cell_phone', models.CharField(max_length=50)),
                ('work_phone', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyParticipationYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
        ),
    ]
