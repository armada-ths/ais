# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-06 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0056_auto_20180406_1215'),
        ('register', '0008_auto_20170831_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlog',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='signuplog',
            name='contact',
        ),
        migrations.AddField(
            model_name='orderlog',
            name='company_contact',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyContact'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signuplog',
            name='company_contact',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyContact'),
            preserve_default=False,
        ),
    ]