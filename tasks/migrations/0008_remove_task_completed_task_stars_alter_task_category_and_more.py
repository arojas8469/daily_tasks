# Generated by Django 5.2 on 2025-06-27 20:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_rename_frequemcy_task_frequency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.AddField(
            model_name='task',
            name='stars',
            field=models.ManyToManyField(blank=True, help_text='Users who have favorited this task', related_name='starred_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Work', 'Work'), ('Personal', 'Personal'), ('Other', 'Other')], default='Work', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, help_text='When this task is due', null=True),
        ),
    ]
