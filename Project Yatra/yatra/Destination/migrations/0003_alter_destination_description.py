# Generated by Django 4.1.5 on 2023-03-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Destination', '0002_rename_is_city_destination_is_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]