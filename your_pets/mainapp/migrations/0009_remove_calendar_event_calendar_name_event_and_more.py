# Generated by Django 5.0.2 on 2024-06-01 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_animalcard_mission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='event',
        ),
        migrations.AddField(
            model_name='calendar',
            name='name_event',
            field=models.CharField(default=1, max_length=200, verbose_name='Событие'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='calendar',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Комментарий'),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
