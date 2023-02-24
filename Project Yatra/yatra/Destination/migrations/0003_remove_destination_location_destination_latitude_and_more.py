# Generated by Django 4.1.5 on 2023-02-24 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Destination', '0002_destination_created_at_destination_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='location',
        ),
        migrations.AddField(
            model_name='destination',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
