from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from organisation.models import DepartmentUser, Location
from tracking.models import CommonFields


@python_2_unicode_compatible
class Vendor(models.Model):
    """Represents the vendor of a product (software or hardware).
    """
    name = models.CharField(
        max_length=256, unique=True, help_text='E.g. Dell, Cisco, etc.')
    details = models.TextField(null=True, blank=True)
    account_rep = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    extra_data = JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Invoice(CommonFields):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    vendor_ref = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="The vendor's reference or invoice number for this order.")
    job_number = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='The P&W job number relating to this order.')
    date = models.DateField(
        blank=True, null=True, help_text='The date shown on the invoice.')
    etj_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='ETJ number.')
    total_value = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True,
        help_text='The total value of the invoice (excluding GST).')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('-job_number',)

    def __str__(self):
        if self.vendor_ref and self.total_value:
            return '{} {} - {:.2f}'.format(self.vendor.name, self.vendor_ref, self.total_value)
        elif self.vendor_ref:
            return '{} - {:.2f}'.format(self.vendor.name, self.total_value)
        else:
            return self.vendor.name


class Asset(CommonFields):
    """Abstract model class to represent fields common to all asset types.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    date_purchased = models.DateField(null=True, blank=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, blank=True, null=True)
    purchased_value = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True,
        help_text='The amount paid for this asset, inclusive of any upgrades (excluding GST).')
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SoftwareLicense(CommonFields):
    """Represents a software licensing arrangement.
    """
    name = models.CharField(max_length=256, unique=True)
    url = models.URLField(max_length=2000, null=True, blank=True)
    support = models.TextField(
        blank=True, help_text='Support timeframe or scope')
    support_url = models.URLField(max_length=2000, null=True, blank=True)
    oss = models.NullBooleanField(
        default=None, help_text='Open-source/free software license?')
    primary_user = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, null=True, blank=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.PROTECT, null=True, blank=True)
    used_licenses = models.PositiveSmallIntegerField(default=0, editable=False)
    available_licenses = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    license_details = models.TextField(
        blank=True, help_text='Direct license keys or details')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class HardwareModel(models.Model):
    """Represents the vendor model type for a physical hardware asset.
    """
    TYPE_CHOICES = (
        ('Air conditioner', 'Air conditioner'),
        ('Camera - Compact', 'Camera - Compact'),
        ('Camera - SLR', 'Camera - SLR'),
        ('Camera - Security (IP)', 'Camera - Security (IP)'),
        ('Camera - Security (non-IP)', 'Camera - Security (non-IP)'),
        ('Camera - Other', 'Camera - Other'),
        ('Chassis', 'Chassis'),
        ('Computer - Desktop', 'Computer - Desktop'),
        ('Computer - Docking station', 'Computer - Docking station'),
        ('Computer - Input device', 'Computer - Input device'),
        ('Computer - Laptop', 'Computer - Laptop'),
        ('Computer - Misc Accessory', 'Computer - Misc Accessory'),
        ('Computer - Monitor', 'Computer - Monitor'),
        ('Computer - Tablet PC', 'Computer - Tablet PC'),
        ('Computer - Other', 'Computer - Other'),
        ('Environmental monitor', 'Environmental monitor'),
        ('Network - Hub', 'Network - Hub'),
        ('Network - Media converter', 'Network - Media converter'),
        ('Network - Modem', 'Network - Modem'),
        ('Network - Module or card', 'Network - Module or card'),
        ('Network - Power injector', 'Network - Power injector'),
        ('Network - Router', 'Network - Router'),
        ('Network - Switch (Ethernet)', 'Network - Switch (Ethernet)'),
        ('Network - Switch (FC)', 'Network - Switch (FC)'),
        ('Network - Wireless AP', 'Network - Wireless AP'),
        ('Network - Wireless bridge', 'Network - Wireless bridge'),
        ('Network - Wireless controller', 'Network - Wireless controller'),
        ('Network - Other', 'Network - Other'),
        ('Phone - Conference', 'Phone - Conference'),
        ('Phone - Desk', 'Phone - Desk'),
        ('Phone - Gateway', 'Phone - Gateway'),
        ('Phone - Mobile', 'Phone - Mobile'),
        ('Phone - Wireless or portable', 'Phone - Wireless or portable'),
        ('Phone - Other', 'Phone - Other'),
        ('Power Distribution Unit', 'Power Distribution Unit'),
        ('Printer - Fax machine', 'Printer - Fax machine'),
        ('Printer - Local', 'Printer - Local'),
        ('Printer - Local Multifunction', 'Printer - Local Multifunction'),
        ('Printer - Multifunction copier', 'Printer - Multifunction copier'),
        ('Printer - Plotter', 'Printer - Plotter'),
        ('Printer - Workgroup', 'Printer - Workgroup'),
        ('Printer - Other', 'Printer - Other'),
        ('Projector', 'Projector'),
        ('Rack', 'Rack'),
        ('Server - Blade', 'Server - Blade'),
        ('Server - Rackmount', 'Server - Rackmount'),
        ('Server - Tower', 'Server - Tower'),
        ('Storage - Disk array', 'Storage - Disk array'),
        ('Storage - NAS', 'Storage - NAS'),
        ('Storage - SAN', 'Storage - SAN'),
        ('Storage - Other', 'Storage - Other'),
        ('Speaker', 'Speaker'),
        ('Tablet', 'Tablet'),
        ('Tape autoloader', 'Tape autoloader'),
        ('Tape drive', 'Tape drive'),
        ('UPS', 'UPS'),
        ('Other', 'Other'),
    )

    model_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    model_no = models.CharField(
        max_length=50,
        help_text="The short model number (eg. '7945G' for a Cisco 7956G phone). Do not enter the class (eg. '7900 series') or the product code (eg. 'WS-7945G=')")
    lifecycle = models.IntegerField(
        help_text="Enter in years how long we should keep items of this model before they get decomissioned. Desktops should generally be three years, servers and networking equipment five years.")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('vendor', 'model_no')

    def __str__(self):
        return '{} {}'.format(self.vendor, self.model_no)


@python_2_unicode_compatible
class HardwareAsset(Asset):
    """Represents a physical hardware asset.
    """
    STATUS_CHOICES = (
        ('In storage', 'In storage'),
        ('Deployed', 'Deployed'),
        ('Disposed', 'Disposed'),
    )
    asset_tag = models.CharField(max_length=10, unique=True)
    finance_asset_tag = models.CharField(
        max_length=10, null=True, blank=True,
        help_text='The Finance Services Branch asset number for (leave blank if unsure).')
    hardware_model = models.ForeignKey(HardwareModel, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='In storage')
    serial = models.CharField(
        max_length=50, help_text='The serial number or service tag.')
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    assigned_user = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ('-asset_tag',)

    def __str__(self):
        return self.asset_tag
