# Generated by Django 3.2.3 on 2021-06-15 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profileEmp', '0005_alter_achievment_profile'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story_task',
            fields=[
                ('id_st', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('type', models.CharField(choices=[('St', 'Story'), ('T', 'Task'), ('Ot', 'other')], max_length=3)),
                ('phase', models.CharField(choices=[('In', 'Intial'), ('D', 'Dev'), ('T', 'Test'), ('Do', 'Documentation'), ('Pr', 'Production'), ('m', 'maintenance'), ('Ot', 'other')], max_length=5)),
                ('State', models.CharField(choices=[('C', 'created'), ('A', 'affected'), ('Inp', 'In progress'), ('D', 'Done'), ('Ca', 'Canceled')], max_length=3)),
                ('nv', models.IntegerField()),
                ('start_before', models.DateField(blank=True, null=True)),
                ('end_before', models.DateField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('duration', models.BigIntegerField(blank=True, help_text='UnixTime', null=True)),
                ('emp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileEmp.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('strat_after_tasks', models.ManyToManyField(blank=True, related_name='_storytask_story_task_strat_after_tasks_+', to='storytask.Story_task')),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id_r', models.BigAutoField(primary_key=True, serialize=False)),
                ('rapport', models.TextField()),
                ('date_add', models.DateField(auto_now_add=True)),
                ('State', models.CharField(choices=[('D', 'Done'), ('Ca', 'Canceled')], max_length=3)),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileEmp.profile')),
                ('story_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storytask.story_task')),
            ],
        ),
    ]
