# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import lib.image


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0063_exhibitor_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='location_at_fair',
            field=models.ImageField(blank=True, upload_to=lib.image.UploadToDirUUID('exhibitors', 'location_at_fair')),
        ),
    ]
