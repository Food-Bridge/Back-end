# Generated by Django 5.0.1 on 2024-01-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_address_jibun_address_address_road_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='building_name',
            field=models.CharField(default=True, max_length=255),
            preserve_default=False,
        ),
    ]
