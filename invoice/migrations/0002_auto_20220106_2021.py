# Generated by Django 3.2.11 on 2022-01-06 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='customer_id',
            new_name='customer_ID',
        ),
        migrations.RenameField(
            model_name='customers',
            old_name='customer_phno',
            new_name='customer_phone_no',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='product_id',
            new_name='product_ID',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='product_rate1',
            new_name='product_rate_1',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='product_rate2',
            new_name='product_rate_2',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='product_rate3',
            new_name='product_rate_3',
        ),
    ]