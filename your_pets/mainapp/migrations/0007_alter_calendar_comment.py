# Generated by Django 5.0.1 on 2024-03-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_advicecard_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий'),
        ),
    ]
