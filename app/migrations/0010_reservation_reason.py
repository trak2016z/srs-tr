# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reason',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
