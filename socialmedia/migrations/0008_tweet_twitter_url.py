# Generated by Django 4.0.5 on 2022-07-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0007_socialmediaposteditem_tweet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='twitter_url',
            field=models.URLField(null=True),
        ),
    ]
