# Generated by Django 4.1.5 on 2023-03-25 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_sosrequest_yatri'),
        ('Food', '0003_alter_food_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorites', to='accounts.yatri'),
        ),
    ]