# Generated by Django 4.2.7 on 2024-04-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0035_course_content_contents_course_content_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='grant',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
