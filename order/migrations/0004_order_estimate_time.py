# Generated by Django 5.0.1 on 2024-04-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_required_options_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimate_time',
            field=models.PositiveIntegerField(default=0),
        ),
    ]