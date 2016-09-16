# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-29 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0037_orgunit_sync_o365'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='orgunit',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='orgunit',
            name='unit_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Department'), (1, 'Division'), (2, 'Branch'), (3, 'Region'), (4, 'Cost Centre'), (5, 'Office'), (6, 'District'), (7, 'Section'), (8, 'Unit'), (9, 'Group'), (10, 'Work centre')], default=4),
        ),
    ]