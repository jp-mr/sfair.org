# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-26 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0011_auto_20170126_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='classlecturenote',
            name='download',
            field=models.IntegerField(default=0),
        ),
    ]
