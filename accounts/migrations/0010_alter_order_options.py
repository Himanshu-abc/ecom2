# Generated by Django 4.0.3 on 2022-04-11 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_order_delivered'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['delivered', 'completed', '-date_ordered']},
        ),
    ]
