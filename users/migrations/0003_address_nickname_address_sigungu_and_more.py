# Generated by Django 5.0.1 on 2024-02-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_address_building_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='sigungu',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('user',), name='Default address unique'),
        ),
    ]
