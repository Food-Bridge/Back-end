# Generated by Django 5.0.1 on 2024-04-02 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_remove_blog_image_blogimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogimage',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='community.blog'),
        ),
    ]
