# Generated by Django 5.0.1 on 2024-03-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_remove_coupon_name_coupon_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=50),
        ),
    ]
