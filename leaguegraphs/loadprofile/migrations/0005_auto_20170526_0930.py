# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadprofile', '0004_matchsummary_game_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchsummary',
            name='game_date',
            field=models.BigIntegerField(),
        ),
    ]
