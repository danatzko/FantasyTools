# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-08 04:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20171208_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='points_away',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='points_home',
            field=models.IntegerField(default=0),
        ),
    ]