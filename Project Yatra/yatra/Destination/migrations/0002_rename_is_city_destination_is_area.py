# Generated by Django 4.1.5 on 2023-03-04 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Destination', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='is_city',
            new_name='is_area',
        ),
    ]
