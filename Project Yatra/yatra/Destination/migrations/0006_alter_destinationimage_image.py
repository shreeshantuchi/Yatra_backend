# Generated by Django 4.1.5 on 2023-02-25 08:21

import Destination.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Destination', '0005_alter_destinationimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationimage',
            name='image',
            field=models.ImageField(upload_to=Destination.models.DestinationImage.nameFile),
        ),
    ]
