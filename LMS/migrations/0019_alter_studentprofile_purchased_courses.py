# Generated by Django 4.2.7 on 2024-02-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0018_alter_course_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='purchased_courses',
            field=models.ManyToManyField(blank=True, to='LMS.course'),
        ),
    ]
