# Generated by Django 4.2.7 on 2024-03-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0025_sponsorprofile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='course_schedule',
            field=models.ManyToManyField(blank=True, to='LMS.course_schedule'),
        ),
    ]
