# Generated by Django 4.1.5 on 2023-03-25 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0006_alter_food_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]