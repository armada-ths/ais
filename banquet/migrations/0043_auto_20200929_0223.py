# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-09-29 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banquet', '0042_afterpartyticket_banquet'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchingInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=255)),
                ('include_in_form', models.BooleanField()),
            ],
            options={
                'ordering': ['interest'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='MatchingProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(max_length=255)),
                ('include_in_form', models.BooleanField()),
            ],
            options={
                'ordering': ['program'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='MatchingYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=255)),
                ('include_in_form', models.BooleanField()),
            ],
            options={
                'ordering': ['year'],
                'default_permissions': [],
            },
        ),
        migrations.RemoveField(
            model_name='tablematching',
            name='catalogue_competences',
        ),
        migrations.RemoveField(
            model_name='tablematching',
            name='catalogue_employments',
        ),
        migrations.RemoveField(
            model_name='tablematching',
            name='catalogue_industries',
        ),
        migrations.RemoveField(
            model_name='tablematching',
            name='catalogue_locations',
        ),
        migrations.RemoveField(
            model_name='tablematching',
            name='catalogue_values',
        ),
        migrations.AddField(
            model_name='tablematching',
            name='matching_interests',
            field=models.ManyToManyField(blank=True, to='banquet.MatchingInterest'),
        ),
        migrations.AddField(
            model_name='tablematching',
            name='matching_program',
            field=models.ManyToManyField(blank=True, to='banquet.MatchingProgram'),
        ),
        migrations.AddField(
            model_name='tablematching',
            name='matching_year',
            field=models.ManyToManyField(blank=True, to='banquet.MatchingYear'),
        ),
    ]