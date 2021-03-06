# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-07 01:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20170817_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwareasset',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hardwaremodel',
            name='lifecycle',
            field=models.IntegerField(help_text='Enter in years how long we should keep items of this model before\n            they get decomissioned. Desktops should generally be three years, servers and\n            networking equipment five years.', verbose_name='lifecycle (years)'),
        ),
        migrations.AlterField(
            model_name='hardwaremodel',
            name='model_no',
            field=models.CharField(help_text="The short model number (eg. '7945G' for a Cisco 7956G phone).\n            Do not enter the class (eg. '7900 series') or the product code (eg. 'WS-7945G=')", max_length=50, verbose_name='model number'),
        ),
        migrations.AlterField(
            model_name='hardwaremodel',
            name='model_type',
            field=models.CharField(choices=[('Air conditioner', 'Air conditioner'), ('Camera - Compact', 'Camera - Compact'), ('Camera - SLR', 'Camera - SLR'), ('Camera - Security (IP)', 'Camera - Security (IP)'), ('Camera - Security (non-IP)', 'Camera - Security (non-IP)'), ('Camera - Other', 'Camera - Other'), ('Chassis', 'Chassis'), ('Computer - Desktop', 'Computer - Desktop'), ('Computer - Docking station', 'Computer - Docking station'), ('Computer - Input device', 'Computer - Input device'), ('Computer - Laptop', 'Computer - Laptop'), ('Computer - Misc Accessory', 'Computer - Misc Accessory'), ('Computer - Monitor', 'Computer - Monitor'), ('Computer - Tablet PC', 'Computer - Tablet PC'), ('Computer - Other', 'Computer - Other'), ('Environmental monitor', 'Environmental monitor'), ('Network - Hub', 'Network - Hub'), ('Network - Media converter', 'Network - Media converter'), ('Network - Modem', 'Network - Modem'), ('Network - Module or card', 'Network - Module or card'), ('Network - Power injector', 'Network - Power injector'), ('Network - Router', 'Network - Router'), ('Network - Switch (Ethernet)', 'Network - Switch (Ethernet)'), ('Network - Switch (FC)', 'Network - Switch (FC)'), ('Network - Wireless AP', 'Network - Wireless AP'), ('Network - Wireless bridge', 'Network - Wireless bridge'), ('Network - Wireless controller', 'Network - Wireless controller'), ('Network - Other', 'Network - Other'), ('Phone - Conference', 'Phone - Conference'), ('Phone - Desk', 'Phone - Desk'), ('Phone - Gateway', 'Phone - Gateway'), ('Phone - Mobile', 'Phone - Mobile'), ('Phone - Wireless or portable', 'Phone - Wireless or portable'), ('Phone - Other', 'Phone - Other'), ('Power Distribution Unit', 'Power Distribution Unit'), ('Printer - Fax machine', 'Printer - Fax machine'), ('Printer - Local', 'Printer - Local'), ('Printer - Local Multifunction', 'Printer - Local Multifunction'), ('Printer - Multifunction copier', 'Printer - Multifunction copier'), ('Printer - Plotter', 'Printer - Plotter'), ('Printer - Workgroup', 'Printer - Workgroup'), ('Printer - Other', 'Printer - Other'), ('Projector', 'Projector'), ('Rack', 'Rack'), ('Server - Blade', 'Server - Blade'), ('Server - Rackmount', 'Server - Rackmount'), ('Server - Tower', 'Server - Tower'), ('Storage - Disk array', 'Storage - Disk array'), ('Storage - NAS', 'Storage - NAS'), ('Storage - SAN', 'Storage - SAN'), ('Storage - Other', 'Storage - Other'), ('Speaker', 'Speaker'), ('Tablet', 'Tablet'), ('Tape autoloader', 'Tape autoloader'), ('Tape drive', 'Tape drive'), ('UPS', 'UPS'), ('Other', 'Other')], help_text='The broad category of this hardware model.', max_length=50),
        ),
        migrations.AlterField(
            model_name='hardwaremodel',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hardwaremodel',
            name='vendor',
            field=models.ForeignKey(help_text='The manufacturer of this hardware model (e.g. Dell, Cisco, Apple).', on_delete=django.db.models.deletion.PROTECT, to='assets.Vendor', verbose_name='manufacturer'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='softwareasset',
            name='license_details',
            field=models.TextField(blank=True, help_text='Description of license arrangement (custodian of license key/s, etc.)', null=True),
        ),
        migrations.AlterField(
            model_name='softwareasset',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='softwareasset',
            name='support',
            field=models.TextField(blank=True, help_text='Description of the scope of vendor support.', null=True),
        ),
    ]
