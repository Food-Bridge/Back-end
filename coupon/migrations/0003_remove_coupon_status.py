# Generated by Django 5.0.1 on 2024-01-27 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_coupon_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='status',
        ),
    ]
