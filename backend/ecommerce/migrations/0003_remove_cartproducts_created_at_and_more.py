# Generated by Django 4.2.6 on 2024-01-25 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_test_product_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproducts',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cartproducts',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='cartproducts',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='cartproducts',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='orderproducts',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='productcolors',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='productcolors',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='productcolors',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='productcolors',
            name='modified_by',
        ),
    ]
