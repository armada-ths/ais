# Generated by Django 2.2.24 on 2024-07-28 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exhibitors', '0071_add_exhibitor_tier'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExhibitorChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('exhibitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exhibitors.Exhibitor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]