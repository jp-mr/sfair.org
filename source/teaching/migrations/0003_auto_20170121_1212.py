# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-21 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0002_auto_20170118_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecode',
            name='title',
            field=models.CharField(default='Curso', max_length=140),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursecode',
            name='code',
            field=models.CharField(max_length=25),
        ),
    ]
