# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor_Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='supervisor_room',
            unique_together=set([('user', 'room')]),
        ),
    ]
