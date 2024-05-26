# Generated by Django 5.0.6 on 2024-05-26 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('datetime_response', models.DateTimeField(auto_now_add=True)),
                ('accept', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('котоняня', 'Котоняня'), ('собаконяня', 'Собаконяня')], max_length=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
            ],
        ),
        migrations.CreateModel(
            name='ServicesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryTrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('postTrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.services')),
            ],
        ),
        migrations.AddField(
            model_name='services',
            name='categories',
            field=models.ManyToManyField(related_name='ServicesCategory', through='core.ServicesCategory', to='core.category'),
        ),
    ]