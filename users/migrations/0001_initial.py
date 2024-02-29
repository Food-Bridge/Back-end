# Generated by Django 5.0.1 on 2024-02-29 17:00

import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0006_alter_restaurant_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(regex='^01[016789]?-?\\d{3,4}-?\\d{4}$')])),
                ('is_seller', models.BooleanField(default=False, verbose_name='판매자 여부')),
                ('grade', models.TextField(default='C', max_length=5)),
                ('order_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(max_length=20)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='profile/resize/%Y/%m/%d')),
                ('image_original', models.ImageField(default='default.png', upload_to='profile/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_address', models.CharField(max_length=255, verbose_name='address')),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('building_name', models.CharField(max_length=255, null=True)),
                ('road_address', models.CharField(blank=True, max_length=255, null=True)),
                ('jibun_address', models.CharField(blank=True, max_length=255, null=True)),
                ('sigungu', models.CharField(blank=True, max_length=255, null=True)),
                ('is_default', models.BooleanField(default=False)),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('user',), name='Default address unique'),
        ),
    ]
