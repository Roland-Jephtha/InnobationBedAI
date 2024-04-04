# Generated by Django 4.2.7 on 2024-03-17 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0022_studentprofile_id_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.studentprofile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]