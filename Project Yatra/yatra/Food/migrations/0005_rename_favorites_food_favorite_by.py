# Generated by Django 4.1.5 on 2023-03-25 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0004_food_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='favorites',
            new_name='favorite_by',
        ),
    ]