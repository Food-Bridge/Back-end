# Generated by Django 5.0.2 on 2024-02-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menu_image_alter_menu_price_menuoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant_image/menu/%Y/%m/%d'),
        ),
    ]