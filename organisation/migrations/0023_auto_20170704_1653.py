# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-04 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0022_auto_20170704_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costcentre',
            name='chart_acct_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='chart of accounts name'),
        ),
    ]
