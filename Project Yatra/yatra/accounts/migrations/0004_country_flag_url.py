# Generated by Django 4.1.5 on 2023-03-01 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_country_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='flag_url',
            field=models.URLField(blank=True),
        ),
    ]
