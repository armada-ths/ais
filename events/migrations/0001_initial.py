# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=500)),
                ('registration_open_time', models.DateTimeField()),
                ('registration_close_time', models.DateTimeField()),
                ('event_start', models.DateTimeField()),
                ('event_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Event_field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('data', models.CharField(max_length=200)),
                ('mandatory', models.BooleanField(default=False)),
                ('position_priority', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
    ]
