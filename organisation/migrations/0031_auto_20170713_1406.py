# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-13 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0030_departmentuser_azure_guid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentuser',
            name='name',
            field=models.CharField(help_text='Format: [Given name] [Surname]', max_length=128),
        ),
    ]
