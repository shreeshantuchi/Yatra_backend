# Generated by Django 4.1.5 on 2023-03-25 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_yatri_favorites_activities_and_more'),
        ('Food', '0007_alter_food_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='favorite_by',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorite_food', to='accounts.yatri'),
        ),
    ]
