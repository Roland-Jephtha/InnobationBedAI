# Generated by Django 4.2.7 on 2024-04-20 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0037_course_schedule_course_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_schedule',
            name='paid',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
