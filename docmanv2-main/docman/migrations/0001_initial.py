# Generated by Django 4.0.3 on 2022-08-29 17:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('notes', models.TextField(blank=True, max_length=1024, null=True)),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 13787), max_length=512)),
                ('is_deleted', models.BooleanField(default=False)),
                ('ordering_id', models.IntegerField(default=0)),
                ('latest_revision', models.DateTimeField(auto_now_add=True)),
                ('file_path', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Relative local path and filename.')),
                ('url', models.URLField(blank=True, max_length=2048, null=True, verbose_name='Full URL to an off-site shared resource.')),
                ('preview_file_path', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Relative local path to pre-generated preview image.')),
                ('permitted_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event_session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('session_type', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, max_length=1024, null=True)),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 11792), max_length=512)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('ordering_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, max_length=1024, null=True)),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 10793), max_length=512)),
                ('ordering_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Event Rooms',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, max_length=16)),
                ('title', models.CharField(blank=True, max_length=1024)),
                ('company', models.CharField(blank=True, max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
                ('read_only_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('presenation_type', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, max_length=1024, null=True)),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 11792), max_length=512)),
                ('ordering_id', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('documents', models.ManyToManyField(blank=True, null=True, to='docman.document')),
                ('presenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docman.room')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='docman.event_session')),
            ],
            options={
                'ordering': ['presenter__last_name'],
            },
        ),
        migrations.AddField(
            model_name='event_session',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docman.room'),
        ),
        migrations.CreateModel(
            name='Event_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=256)),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 9796), max_length=512)),
                ('ordering_id', models.IntegerField(default=0)),
                ('presentations', models.ManyToManyField(blank=True, to='docman.presentation')),
                ('sessions', models.ManyToManyField(blank=True, to='docman.event_session')),
            ],
            options={
                'verbose_name': 'Event Day',
                'verbose_name_plural': 'Event Days',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=datetime.datetime(2022, 8, 29, 13, 33, 8, 4811), max_length=512)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, max_length=1024, null=True)),
                ('admins', models.ManyToManyField(blank=True, related_name='admin_events', to=settings.AUTH_USER_MODEL)),
                ('days', models.ManyToManyField(blank=True, to='docman.event_day')),
                ('presenters', models.ManyToManyField(blank=True, related_name='presenter_events', to=settings.AUTH_USER_MODEL)),
                ('rooms', models.ManyToManyField(blank=True, related_name='event_rooms', to='docman.room')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Global event setup',
            },
        ),
    ]
