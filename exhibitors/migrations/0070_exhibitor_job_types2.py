# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    def update_offers(apps, scema_editor):
        Question = apps.get_model('matching', 'Question')
        Response = apps.get_model('matching', 'Response')
        IntegerAns = apps.get_model('matching', 'IntegerAns')
        JobType = apps.get_model('exhibitors', 'JobType')

        summer_job_question = Question.objects.filter(name='Number of ').first()
        master_thesis_question = Question.objects.filter(name='Number of mast').first()
        part_time_job_question = Question.objects.filter(name='Number of part t').first()
        trainee_question = Question.objects.filter(name='Number of tr').first()
        job_types = [summer_job_question, master_thesis_question, part_time_job_question, trainee_question]

        for answer in IntegerAns.objects.filter(question__in=job_types):
            if answer.ans >=1:
                exhibitor = answer.response.exhibitor
                if answer.question == summer_job_question:
                    exhibitor.job_types.add(JobType.objects.get(name='Summer Jobs'))
                if answer.question == master_thesis_question:
                    exhibitor.job_types.add(JobType.objects.get(name="Master's Thesis"))
                if answer.question == part_time_job_question:
                    exhibitor.job_types.add(JobType.objects.get(name='Part-time Jobs'))
                if answer.question == trainee_question:
                    exhibitor.job_types.add(JobType.objects.get(name='Trainee Employment'))
                exhibitor.save()

    dependencies = [
        ('exhibitors', '0069_exhibitor_job_types'),
        ('matching', '0031_auto_20171030_1602')
    ]

    operations = [
        migrations.RunPython(update_offers)

    ]



