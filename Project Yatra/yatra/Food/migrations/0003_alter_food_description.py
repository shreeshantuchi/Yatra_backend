# Generated by Django 4.1.5 on 2023-03-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0002_alter_food_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
