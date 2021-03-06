# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-26 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0005_auto_20170126_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_time',
            field=models.TimeField(max_length=50),
        ),
        migrations.AlterField(
            model_name='class',
            name='classroom',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='class',
            name='duration',
            field=models.CharField(choices=[('sem1', 'S1'), ('sem2', 'S2'), ('annual', 'Annual')], max_length=10),
        ),
        migrations.AlterField(
            model_name='class',
            name='infobox_title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='classlecturenotes',
            name='position',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
    ]
