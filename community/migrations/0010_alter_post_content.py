# Generated by Django 5.0.1 on 2024-04-16 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_alter_postimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]
