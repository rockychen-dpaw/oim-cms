# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0007_auto_20170323_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentuser',
            name='ad_guid',
            field=models.CharField(editable=False, help_text='Locally stored GUID. This field must match GUID in the AD object for sync to be successful', max_length=48, unique=True),
        ),
    ]
