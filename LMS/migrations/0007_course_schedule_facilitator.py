# Generated by Django 4.2.3 on 2024-01-30 04:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0006_alter_course_schedule_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_schedule',
            name='facilitator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
