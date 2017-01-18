# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.9.5 on 2017-01-14 19:50
=======
# Generated by Django 1.9.5 on 2016-10-19 16:41
>>>>>>> da58414e215eef7307c6e490e92b649f26b36474
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('title', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=1000)),
                ('journal', models.CharField(max_length=500)),
                ('year', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=2017)),
                ('abstract', models.TextField()),
                ('upload', models.FileField(blank=True, max_length=300, upload_to='publications')),
=======
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=300)),
                ('journal', models.CharField(max_length=500)),
                ('year', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016)], default=2016)),
                ('abstract', models.TextField()),
                ('upload', models.FileField(blank=True, null=True, upload_to='publications')),
>>>>>>> da58414e215eef7307c6e490e92b649f26b36474
                ('download', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-year', 'id'],
            },
        ),
    ]
