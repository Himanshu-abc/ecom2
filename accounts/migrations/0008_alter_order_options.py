# Generated by Django 4.0.3 on 2022-04-11 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['completed', '-date_ordered']},
        ),
    ]
