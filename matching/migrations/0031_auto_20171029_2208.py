# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0030_merge_20171027_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('job_type', models.TextField()),
                ('job_type_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('name', models.TextField()),
                ('region_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerJobType',
            fields=[
                ('studentanswerbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matching.StudentAnswerBase')),
                ('job_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.JobType')),
            ],
            bases=('matching.studentanswerbase',),
        ),
        migrations.AlterModelOptions(
            name='studentanswerbase',
            options={'default_permissions': (), 'verbose_name': 'answers base'},
        ),
        migrations.AlterModelOptions(
            name='studentanswergrading',
            options={'default_permissions': (), 'verbose_name': 'answer grading', 'verbose_name_plural': 'answers grading'},
        ),

        migrations.AlterModelOptions(
            name='studentanswerslider',
            options={'default_permissions': (), 'verbose_name': 'answer slider', 'verbose_name_plural': 'answers slider'},
        ),
        migrations.AlterModelOptions(
            name='studentanswerworkfield',
            options={'default_permissions': (), 'verbose_name': 'answer workfield', 'verbose_name_plural': 'answers workfield'},
        ),
        migrations.RemoveField(
            model_name='continent',
            name='name',
        ),
        migrations.AlterField(
            model_name='studentanswergrading',
            name='answer',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='studentanswerregion',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.Region'),
        ),
        migrations.AlterField(
            model_name='studentanswerslider',
            name='answer_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='swedencity',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.Region'),
        ),
        migrations.DeleteModel(
            name='StudentAnswerContinent',
        ),
        migrations.DeleteModel(
            name='SwedenRegion',
        ),
        migrations.AddField(
            model_name='continent',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.Region'),
        ),
    ]
