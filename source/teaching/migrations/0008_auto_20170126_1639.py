# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-26 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0007_auto_20170126_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlecturenotes',
            name='position',
            field=models.PositiveSmallIntegerField(),
        ),
    ]