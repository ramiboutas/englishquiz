# Generated by Django 4.2.4 on 2023-10-30 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0017_book_image_book_promoted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='book',
            name='thumbnail_url',
        ),
    ]
