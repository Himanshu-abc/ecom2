# Generated by Django 4.0.3 on 2022-04-11 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_rename_shippingaddress_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.order'),
        ),
    ]