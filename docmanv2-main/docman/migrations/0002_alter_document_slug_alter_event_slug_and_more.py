# Generated by Django 4.0.3 on 2022-08-29 18:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 221880), max_length=512),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 213198), max_length=512),
        ),
        migrations.AlterField(
            model_name='event_day',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 218888), max_length=512),
        ),
        migrations.AlterField(
            model_name='event_session',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 220883), max_length=512),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 220883), max_length=512),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.CharField(default=datetime.datetime(2022, 8, 29, 14, 57, 4, 219886), max_length=512),
        ),
    ]
