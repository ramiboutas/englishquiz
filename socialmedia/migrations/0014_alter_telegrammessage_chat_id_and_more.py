# Generated by Django 4.0.5 on 2022-07-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0013_remove_regularsocialpost_promote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrammessage',
            name='chat_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='telegrammessage',
            name='link',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='telegrammessage',
            name='message_id',
            field=models.BigIntegerField(),
        ),
    ]