# Generated by Django 5.0.1 on 2024-04-28 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='menu_list',
            new_name='cart_list',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='option_list',
        ),
    ]
