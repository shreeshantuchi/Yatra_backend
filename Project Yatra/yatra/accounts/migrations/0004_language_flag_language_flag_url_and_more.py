# Generated by Django 4.1.5 on 2023-03-05 12:28

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_interest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='flag',
            field=models.ImageField(blank=True, upload_to=accounts.models.Language.nameFile),
        ),
        migrations.AddField(
            model_name='language',
            name='flag_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='sahayatriexpert',
            name='languages',
            field=models.ManyToManyField(to='accounts.language'),
        ),
        migrations.AddField(
            model_name='sahayatriguide',
            name='languages',
            field=models.ManyToManyField(to='accounts.language'),
        ),
        migrations.AddField(
            model_name='yatri',
            name='languages',
            field=models.ManyToManyField(to='accounts.language'),
        ),
        migrations.AlterField(
            model_name='sahayatriguide',
            name='interests',
            field=models.ManyToManyField(related_name='interest_guide', to='accounts.interest'),
        ),
        migrations.AlterField(
            model_name='yatri',
            name='interests',
            field=models.ManyToManyField(related_name='interest_yatri', to='accounts.interest'),
        ),
    ]
