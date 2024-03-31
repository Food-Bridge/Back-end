# Generated by Django 5.0.2 on 2024-03-03 13:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': '대분류',
                'verbose_name_plural': '대분류',
            },
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'verbose_name': '매장', 'verbose_name_plural': '매장'},
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='reviewCouunt',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='delivertyFee',
            field=models.PositiveIntegerField(default=0, verbose_name='배달 요금'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='minPickupTime',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='최소 픽업 시간'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='minimumPickupPrice',
            field=models.PositiveIntegerField(default=0, verbose_name=' 픽업 최소 주문 금액'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='reviewCount',
            field=models.PositiveIntegerField(default=0, verbose_name='리뷰수'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=255, verbose_name='매장 주소'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='bookmarkCount',
            field=models.PositiveIntegerField(default=0, verbose_name='즐겨찾기수'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.CharField(blank=True, max_length=255, verbose_name='매장 설명'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='end',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 36), django.core.validators.MaxValueValidator(36)], verbose_name='영업 마감 시간'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, default='default_restaurant.png', null=True, upload_to='restaurant_image/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='maxDeliveryTime',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='최대 배달 시간'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='minDeliveryTime',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='최소 배달 시간'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='minimumOrderPrice',
            field=models.PositiveIntegerField(default=0, verbose_name='최소 주문 금액'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255, verbose_name='매장 이름'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='operatingTime',
            field=models.CharField(max_length=255, verbose_name='운영 시간 설명'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='orderCount',
            field=models.PositiveIntegerField(default=0, verbose_name='주문수'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='packaging',
            field=models.BooleanField(default=False, verbose_name='포장 여부'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^02?-?\\d{3,4}-?\\d{4}$')], verbose_name='매장 전화번호'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, 5), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='start',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 24), django.core.validators.MaxValueValidator(24)], verbose_name='영업 시작 시간'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='status',
            field=models.BooleanField(default=False, verbose_name='매장 운영 여부'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='mainCategory',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='mainCategory', to='restaurant.maincategory', verbose_name='매장 대분류'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('main_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.maincategory')),
            ],
            options={
                'verbose_name': '중분류',
                'verbose_name_plural': '중분류',
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='subCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subCategory', to='restaurant.subcategory', verbose_name='매장 중분류'),
        ),
    ]