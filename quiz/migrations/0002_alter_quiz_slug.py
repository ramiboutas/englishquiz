# Generated by Django 4.0.3 on 2022-04-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
