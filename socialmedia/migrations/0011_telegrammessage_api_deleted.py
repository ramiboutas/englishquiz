# Generated by Django 4.0.5 on 2022-07-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0010_telegrammessage_api_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrammessage',
            name='api_deleted',
            field=models.BooleanField(default=False, verbose_name='Already deleted from Telegram'),
        ),
    ]
