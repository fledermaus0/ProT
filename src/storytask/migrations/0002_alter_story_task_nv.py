# Generated by Django 3.2.3 on 2021-06-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storytask', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story_task',
            name='nv',
            field=models.IntegerField(default=1),
        ),
    ]