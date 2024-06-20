# Generated by Django 5.0.6 on 2024-06-19 10:43

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_customer_sit_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cat_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('boarding', 'Передержка'), ('walk', 'Выгул'), ('daycare', 'Няня'), ('dogsitter', 'Собака'), ('catsitter', 'Кошка')], max_length=100, null=True, verbose_name='Выберите вид оказываемой услуги и вид питомца, с которым хотели бы заниматься'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sit_pet',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('кошка', 'кошка'), ('собака', 'собака'), ('отсутствуют', 'отсутствуют')], max_length=50, null=True),
        ),
    ]