# Generated by Django 4.2.4 on 2023-10-29 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0038_rename_created_socialpost_created_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BackgroundImage',
        ),
        migrations.DeleteModel(
            name='LinkedinPost',
        ),
        migrations.DeleteModel(
            name='TelegramMessage',
        ),
    ]