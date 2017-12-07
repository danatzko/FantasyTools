# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-06 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('pos', models.CharField(max_length=5)),
                ('team', models.CharField(max_length=1)),
                ('oppt', models.CharField(max_length=5)),
                ('salary', models.IntegerField(default=0)),
                ('h_a', models.CharField(max_length=1)),
                ('points', models.FloatField(default=0)),
            ],
        ),
    ]
