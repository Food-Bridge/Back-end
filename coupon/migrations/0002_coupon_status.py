# Generated by Django 5.0.1 on 2024-01-27 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
