# Generated by Django 2.2.12 on 2022-04-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20220421_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
