# Generated by Django 4.2.7 on 2024-03-20 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0024_course_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorprofile',
            name='bio',
            field=models.TextField(null=True),
        ),
    ]