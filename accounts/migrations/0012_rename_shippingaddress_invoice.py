# Generated by Django 4.0.3 on 2022-04-11 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0011_shippingaddress_email_shippingaddress_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAddress',
            new_name='Invoice',
        ),
    ]
