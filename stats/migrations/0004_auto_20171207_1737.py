# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-07 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20171207_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestats',
            name='Player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='stats.Player'),
        ),
    ]