# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion



def add_jobtypes(apps, schema_editor):
	JobType = apps.get_model('matching', 'JobType')
	for i in range(1,5):
		try:
			JobType.objects.filter(job_type_id=i).delete()
		except:
			pass

	JobType.objects.get_or_create(job_type='master thesis', job_type_id='1')
	JobType.objects.get_or_create(job_type='part time job', job_type_id='2')
	JobType.objects.get_or_create(job_type='trainee', job_type_id='3')
	JobType.objects.get_or_create(job_type='summer job', job_type_id='4')

class Migration(migrations.Migration):

  dependencies = [
      ('matching', '0034_jobtype_studentanswerjobtype'),
  ]

  operations = [
    migrations.RunPython(add_jobtypes),
  ]
