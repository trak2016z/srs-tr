# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 15:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20161102_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='0', max_length=1)),
                ('considered_date', models.DateTimeField(null=True)),
                ('considered_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='considered', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Room')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
