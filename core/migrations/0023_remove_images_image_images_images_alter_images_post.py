# Generated by Django 5.0.6 on 2024-06-16 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_customer_about_me_alter_customer_bio_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='image',
        ),
        migrations.AddField(
            model_name='images',
            name='images',
            field=models.ImageField(blank=True, upload_to='images/gallery/%Y/%m/%d/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PostsImages', to='core.customer'),
        ),
    ]
