# Generated by Django 4.2.3 on 2024-02-24 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0012_course_schedule_link_alter_course_schedule_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='purchased_courses',
            field=models.ManyToManyField(null=True, to='LMS.course'),
        ),
    ]