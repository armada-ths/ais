# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-29 20:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markupfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('companies', '0002_auto_20180729_2211'),
        ('fair', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', markupfield.fields.MarkupField(rendered_field=True)),
                ('question_markup_type', models.CharField(choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown')], default='markdown', editable=False, max_length=30)),
                ('field_type', models.CharField(choices=[('text_field', 'Text field'), ('check_box', 'Check box'), ('text_area', 'Text area'), ('radio_buttons', 'Radio buttons'), ('select', 'Drop-down list'), ('file', 'File'), ('image', 'Image')], default='text_field', max_length=20)),
                ('position', models.IntegerField(default=0)),
                ('_question_rendered', models.TextField(editable=False)),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFieldAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('custom_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.CustomField')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFieldArgument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('position', models.IntegerField(default=0)),
                ('custom_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.CustomField')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('interview_date', models.DateTimeField(blank=True, null=True)),
                ('interview_location', models.CharField(blank=True, max_length=100, null=True)),
                ('submission_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('scorecard', models.CharField(blank=True, max_length=300, null=True)),
                ('drive_document', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], max_length=20, null=True)),
            ],
            options={
                'permissions': (('administer_recruitment_applications', 'Administer recruitment applications'), ('view_recruitment_applications', 'View recruitment applications'), ('view_recruitment_interviews', 'View recruitment interviews')),
            },
        ),
        migrations.CreateModel(
            name='RecruitmentApplicationComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('recruitment_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.RecruitmentApplication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('interview_end_date', models.DateTimeField()),
                ('eligible_roles', models.IntegerField(default=3)),
                ('allowed_groups', models.ManyToManyField(help_text='Only those who are members of at least one of the selected groups can see the applications submitted to this recruitment period.', to='auth.Group')),
                ('application_questions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_questions', to='recruitment.ExtraField')),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
                ('interview_questions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.ExtraField')),
            ],
            options={
                'permissions': (('administer_recruitment', 'Administer recruitment'),),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('organization_group', models.CharField(default='', max_length=100, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('parent_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.Role')),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('administer_roles', 'Administer roles'),),
            },
        ),
        migrations.CreateModel(
            name='RoleApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('recruitment_application', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='recruitment.RecruitmentApplication')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.Role')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='recruitmentperiod',
            name='recruitable_roles',
            field=models.ManyToManyField(to='recruitment.Role'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='delegated_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delegated_role', to='recruitment.Role'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='exhibitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='interviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='interviewer2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviewer2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='recommended_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.Role'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='recruitment_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.RecruitmentPeriod'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='superior_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='superior_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customfield',
            name='extra_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.ExtraField'),
        ),
    ]
