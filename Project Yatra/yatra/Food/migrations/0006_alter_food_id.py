# Generated by Django 4.1.5 on 2023-03-25 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0005_rename_favorites_food_favorite_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
