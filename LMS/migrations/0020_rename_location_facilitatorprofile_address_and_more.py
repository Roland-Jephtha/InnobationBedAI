# Generated by Django 4.2.7 on 2024-02-26 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0019_alter_studentprofile_purchased_courses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facilitatorprofile',
            old_name='location',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='sponsorprofile',
            old_name='location',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='location',
            new_name='address',
        ),
    ]
