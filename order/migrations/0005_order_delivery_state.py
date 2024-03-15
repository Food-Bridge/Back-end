# Generated by Django 5.0.1 on 2024-03-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_rename_paymentmethod_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_state',
            field=models.CharField(choices=[('waiting', '대기'), ('pickup_complete', '포장완료'), ('delivery_complete', '배달완료')], default='대기', max_length=20, verbose_name='포장배달 상태'),
        ),
    ]
