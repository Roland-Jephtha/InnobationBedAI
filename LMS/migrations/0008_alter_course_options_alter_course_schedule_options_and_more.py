# Generated by Django 4.2.3 on 2024-01-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0007_course_schedule_facilitator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='course_schedule',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='facilitatorprofile',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='sponsorprofile',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='studentprofile',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='course',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='course_schedule',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='facilitatorprofile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sponsorprofile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
