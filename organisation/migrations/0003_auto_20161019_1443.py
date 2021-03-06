# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-19 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_departmentuser_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentuser',
            name='o365_licence',
            field=models.NullBooleanField(default=None, editable=False, help_text='Account consumes an Office 365 licence.'),
        ),
        migrations.AddField(
            model_name='departmentuser',
            name='shared_account',
            field=models.BooleanField(default=False, editable=False, help_text='Automatically set from account type.'),
        ),
    ]
