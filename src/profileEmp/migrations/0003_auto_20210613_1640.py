# Generated by Django 3.2.3 on 2021-06-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileEmp', '0002_alter_profile_sal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='CV',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
