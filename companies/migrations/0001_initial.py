# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('organisation_number', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('cell_phone', models.CharField(max_length=50)),
                ('work_phone', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='companies.Company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyParticipationYear',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('company', models.ForeignKey(to='companies.Company')),
                ('fair', models.ForeignKey(to='fair.Fair')),
            ],
        ),
    ]
