# Generated by Django 4.2.3 on 2024-02-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0010_remove_customuser_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_schedule',
            name='duration',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
