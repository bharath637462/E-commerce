# Generated by Django 4.2.6 on 2024-02-25 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_remove_cartproducts_quantity_cartproducts_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartproducts',
            old_name='product',
            new_name='products',
        ),
    ]
