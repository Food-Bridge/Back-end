# Generated by Django 5.0.1 on 2024-03-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_deliveryman_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='paymentMethod',
            new_name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='deliver_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_deliver',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]