# Generated by Django 5.0.6 on 2024-06-17 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_delete_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/gallery/%Y/%m/%d/')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.customer')),
            ],
        ),
    ]