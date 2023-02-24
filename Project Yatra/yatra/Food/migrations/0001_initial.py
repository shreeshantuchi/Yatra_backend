# Generated by Django 4.1.5 on 2023-02-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('LOC', 'Local food provider'), ('RST', 'Restaurant'), ('CAF', 'Cafe'), ('BAK', 'Bakery'), ('FTK', 'Food truck'), ('OTH', 'Others')], default='OTH', max_length=50)),
                ('phone_no', models.CharField(default='XXXXXXXXXX', max_length=20)),
                ('average_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('related_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
