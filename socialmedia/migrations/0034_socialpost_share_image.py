# Generated by Django 4.2.4 on 2023-10-03 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0033_socialpost_background_image_obj'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialpost',
            name='share_image',
            field=models.BooleanField(default=False),
        ),
    ]