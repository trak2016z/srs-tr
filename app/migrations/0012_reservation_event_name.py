# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_availability_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='event_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
