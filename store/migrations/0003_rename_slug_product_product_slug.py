# Generated by Django 4.1.7 on 2023-03-20 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='product_slug',
        ),
    ]