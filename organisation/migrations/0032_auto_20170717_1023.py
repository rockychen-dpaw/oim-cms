# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-17 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0031_auto_20170713_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentuser',
            name='ad_deleted',
            field=models.BooleanField(default=False, editable=False, help_text='Account has been deleted in Active Directory.', verbose_name='AD deleted'),
        ),
        migrations.AlterField(
            model_name='departmentuser',
            name='ad_dn',
            field=models.CharField(blank=True, help_text='AD DistinguishedName value.', max_length=512, null=True, unique=True, verbose_name='AD DN'),
        ),
        migrations.AlterField(
            model_name='departmentuser',
            name='ad_guid',
            field=models.CharField(blank=True, help_text='Locally stored AD GUID. This field must match GUID in the AD object for sync to be successful', max_length=48, null=True, unique=True, verbose_name='AD GUID'),
        ),
        migrations.AlterField(
            model_name='departmentuser',
            name='azure_guid',
            field=models.CharField(blank=True, help_text='Azure AD GUID.', max_length=48, null=True, unique=True, verbose_name='Azure GUID'),
        ),
        migrations.AlterField(
            model_name='departmentuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
