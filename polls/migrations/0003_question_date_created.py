# Generated by Django 5.0.4 on 2024-04-30 23:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20221205_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
