# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-01 21:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_group_is_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('shirt_size', models.CharField(blank=True, choices=[('WXS', 'Woman X-Small'), ('WS', 'Woman Small'), ('WM', 'Woman Medium'), ('WL', 'Woman Large'), ('WXL', 'Woman X-Large'), ('MXS', 'Man X-Small'), ('MS', 'Man Small'), ('MM', 'Man Medium'), ('ML', 'Man Large'), ('MXL', 'Man X-Large')], max_length=3)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('drivers_license', models.CharField(blank=True, max_length=10, null=True)),
                ('allergy', models.CharField(blank=True, max_length=30, null=True)),
                ('programme', models.CharField(blank=True, max_length=30, null=True)),
                ('registration_year', models.IntegerField(blank=True, null=True)),
                ('planned_graduation', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
