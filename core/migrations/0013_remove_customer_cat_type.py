# Generated by Django 5.0.6 on 2024-06-10 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_customer_area_customer_cat_type_customer_dob_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='cat_type',
        ),
    ]
