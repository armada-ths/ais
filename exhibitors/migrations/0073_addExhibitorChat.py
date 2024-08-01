# Generated by Django 2.2.24 on 2024-07-28 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0072_addExhibitorChat'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitorchat',
            name='is_armada_response',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exhibitorchat',
            name='exhibitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exhibitors.Exhibitor'),
        ),
        migrations.AlterField(
            model_name='exhibitorchat',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
