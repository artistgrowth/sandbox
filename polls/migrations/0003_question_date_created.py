# Generated by Django 4.2.13 on 2024-05-15 00:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("polls", "0002_auto_20221205_2153")]

    operations = [
        migrations.AddField(
            model_name="question",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        )
    ]
