# Generated by Django 2.2.12 on 2022-04-04 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220404_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Address'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Address'),
        ),
    ]
