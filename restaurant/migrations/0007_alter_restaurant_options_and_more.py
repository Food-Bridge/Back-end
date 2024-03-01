# Generated by Django 5.0.2 on 2024-03-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_alter_restaurant_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'verbose_name': '음식점', 'verbose_name_plural': '음식점'},
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='reviewCouunt',
            new_name='reviewCount',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='delivertyFee',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, default='default_restaurant.png', null=True, upload_to='restaurant_image/%Y/%m/%d'),
        ),
    ]