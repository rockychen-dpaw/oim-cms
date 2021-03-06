# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-13 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0031_auto_20170713_1406'),
        ('registers', '0019_itsystemevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsystemevent',
            name='it_systems',
            field=models.ManyToManyField(blank=True, help_text='IT System(s) affect by this event', to='registers.ITSystem'),
        ),
        migrations.AddField(
            model_name='itsystemevent',
            name='locations',
            field=models.ManyToManyField(blank=True, help_text='Location(s) affect by this event', to='organisation.Location'),
        ),
    ]
