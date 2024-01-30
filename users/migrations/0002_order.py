# Generated by Django 5.0.1 on 2024-01-29 16:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_restaurant_maxdeliverytime_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('requests', models.TextField()),
                ('paymentMethod', models.CharField(choices=[('credit_card', '신용 카드'), ('cash', '현금')], max_length=20)),
                ('totalPrice', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
