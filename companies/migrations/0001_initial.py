# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-29 20:11
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Organisation name')),
                ('identity_number', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Companies',
                'permissions': (('base', 'Companies'),),
            },
        ),
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('INVOICE', 'Invoice'), ('TRANSPORT', 'Transport'), ('OFFICE', 'Office')], max_length=200)),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name, if different from the organisation name')),
                ('street', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(choices=[('DENMARK', 'Denmark'), ('FINLAND', 'Finland'), ('FRANCE', 'France'), ('GERMANY', 'Germany'), ('NORWAY', 'Norway'), ('SWEDEN', 'Sweden'), ('UNITED_KINGDOM', 'United Kingdom')], default='SWEDEN', max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('email_address', models.CharField(blank=True, max_length=200, null=True, verbose_name='E-mail address')),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Company addresses',
            },
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, null=True, verbose_name='First name')),
                ('last_name', models.CharField(max_length=200, null=True, verbose_name='Last name')),
                ('email_address', models.EmailField(max_length=200, verbose_name='E-mail address')),
                ('alternative_email_address', models.EmailField(blank=True, max_length=200, null=True, verbose_name='Alternative e-mail address')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile_phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('work_phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['company__name'],
                'verbose_name_plural': 'Company customers',
            },
        ),
        migrations.CreateModel(
            name='CompanyCustomerComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CompanyCustomerResponsible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['company__name', 'group__name'],
                'verbose_name_plural': 'Company customer responsibles',
            },
        ),
        migrations.CreateModel(
            name='CompanyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['type'],
                'verbose_name_plural': 'Company types',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_full', models.CharField(editable=False, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('color', models.CharField(blank=True, choices=[('BLUE', 'Blue'), ('GREEN', 'Green'), ('RED', 'Red'), ('YELLOW', 'Yellow')], max_length=200, null=True)),
                ('allow_companies', models.BooleanField(default=True)),
                ('allow_registration', models.BooleanField(default=False)),
                ('allow_responsibilities', models.BooleanField(default=False)),
                ('allow_comments', models.BooleanField(default=False)),
                ('allow_statistics', models.BooleanField(default=False)),
                ('allow_status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['parent__name', 'name'],
                'verbose_name_plural': 'Groups',
            },
        ),
    ]
