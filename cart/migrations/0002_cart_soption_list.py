# Generated by Django 5.0.1 on 2024-04-14 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='soption_list',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
