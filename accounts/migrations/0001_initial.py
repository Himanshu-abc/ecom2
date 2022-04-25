# Generated by Django 2.2.12 on 2022-04-01 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True, blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('date_ordered', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shopkeeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Address')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('available', models.BooleanField(blank=True, default=True, null=True)),
                ('image', models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('shopkeeper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Shopkeeper')),
                ('tags', models.ManyToManyField(to='accounts.Tag')),
            ],
            options={
                'ordering': ('date_added', 'product_name'),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Address')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
                'abstract': False,
            },
        ),
    ]