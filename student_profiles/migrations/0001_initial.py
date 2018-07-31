# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exhibitors', '0001_initial'),
        ('fair', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchingResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('exhibitor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exhibitors.Exhibitor')),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
            options={
                'verbose_name': 'results matching',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=512)),
                ('linkedin_profile', models.CharField(blank=True, max_length=128, null=True)),
                ('facebook_profile', models.CharField(blank=True, max_length=128, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='matchingresult',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_profiles.StudentProfile'),
        ),
    ]
