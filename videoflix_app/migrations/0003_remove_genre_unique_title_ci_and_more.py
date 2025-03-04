# Generated by Django 5.1.4 on 2025-02-21 11:49

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0002_videoprogress'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='genre',
            name='unique_title_ci',
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('title'), name='unique_title_ci_genre'),
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('title'), name='unique_title_ci_video'),
        ),
    ]
