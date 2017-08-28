# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fair', '0005_fair_current'),
        ('exhibitors', '0054_auto_20170607_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.CharField(choices=[('text', 'text'), ('select', 'select'), ('integer', 'integer'), ('boolean', 'boolean')], max_length=256)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.Category')),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exhibitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exhibitors.Exhibitor')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BooleanAns',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matching.Answer')),
                ('ans', models.BooleanField(choices=[(True, 'yes'), (False, 'no')])),
            ],
            bases=('matching.answer',),
        ),
        migrations.CreateModel(
            name='ChoiceAns',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matching.Answer')),
                ('ans', models.IntegerField(blank=True, choices=[(1, 'Definitely Not'), (2, 'Probably Not'), (3, 'Maybe'), (4, 'Probably'), (5, 'Definitely')], null=True)),
            ],
            bases=('matching.answer',),
        ),
        migrations.CreateModel(
            name='IntegerAns',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matching.Answer')),
                ('ans', models.IntegerField(blank=True, null=True)),
            ],
            bases=('matching.answer',),
        ),
        migrations.CreateModel(
            name='TextAns',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='matching.Answer')),
                ('ans', models.CharField(blank=True, max_length=50, null=True)),
            ],
            bases=('matching.answer',),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matching.Survey'),
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.Response'),
        ),
    ]
