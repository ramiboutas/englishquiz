# Generated by Django 4.0.4 on 2022-04-22 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_lection_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.TextField(),
        ),
    ]
