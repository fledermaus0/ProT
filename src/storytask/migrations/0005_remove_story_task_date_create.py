# Generated by Django 3.2.3 on 2021-06-26 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storytask', '0004_story_task_date_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story_task',
            name='date_create',
        ),
    ]
