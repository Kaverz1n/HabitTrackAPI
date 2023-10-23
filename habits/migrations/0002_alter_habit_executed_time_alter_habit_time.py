# Generated by Django 4.2.6 on 2023-10-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='executed_time',
            field=models.TimeField(default='00:02:00', verbose_name='время на выполнение'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='time',
            field=models.TimeField(verbose_name='время'),
        ),
    ]
