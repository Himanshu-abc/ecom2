# Generated by Django 2.2.12 on 2022-04-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_invoice_email_alter_invoice_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
