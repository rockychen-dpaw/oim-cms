# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-14 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0005_auto_20161013_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsystem',
            name='other_projects',
            field=models.TextField(blank=True, help_text='Details of related IT Systems and projects.', null=True),
        ),
    ]
