# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-29 20:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
        ('fair', '0001_initial'),
        ('register', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register.SignupContract'),
        ),
        migrations.AddField(
            model_name='group',
            name='fair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companylog',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='companylog',
            name='fair',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fair.Fair'),
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companycustomerresponsible',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companycustomercomment',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='companycustomercomment',
            name='groups',
            field=models.ManyToManyField(blank=True, to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companycustomercomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companycustomer',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='companycustomer',
            name='fair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair'),
        ),
        migrations.AddField(
            model_name='companycustomer',
            name='groups',
            field=models.ManyToManyField(to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companycustomer',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status', to='companies.Group'),
        ),
        migrations.AddField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='companycontact',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companyaddress',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='company',
            name='groups',
            field=models.ManyToManyField(to='companies.Group'),
        ),
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyType'),
        ),
        migrations.AlterUniqueTogether(
            name='companycustomerresponsible',
            unique_together=set([('company', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='companycustomer',
            unique_together=set([('company', 'fair')]),
        ),
    ]
