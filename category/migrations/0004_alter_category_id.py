# Generated by Django 4.1.7 on 2023-03-23 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_auto_20230321_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
