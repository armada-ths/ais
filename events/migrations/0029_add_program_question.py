# Generated by Django 2.2.24 on 2023-10-18 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20210918_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupquestion',
            name='type',
            field=models.CharField(choices=[('text_field', 'Short Text'), ('text_area', 'Long Text'), ('single_choice', 'Single Choice'), ('multiple_choice', 'Multiple Choice'), ('student_program', 'Student Program')], max_length=20),
        ),
    ]
