# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-07 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import lib.image


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20161006_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_original',
            field=models.ImageField(blank=True, upload_to=lib.image.UploadToDirUUID('events', 'image_original')),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, upload_to=lib.image.UploadToDir('events', 'image')),
        ),
    ]
