# Generated by Django 4.2.7 on 2024-03-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0028_alter_course_schedule_course_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
