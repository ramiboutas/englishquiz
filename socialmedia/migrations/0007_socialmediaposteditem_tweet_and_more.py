# Generated by Django 4.0.5 on 2022-07-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0006_regularsocialpost_image_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaPostedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.SmallIntegerField(blank=True, choices=[(1, 'Blog post promotion'), (2, 'Regular social post promotion'), (3, 'Scheduled social post promotion'), (4, 'Scheduled social post promotion')], null=True)),
                ('linkedin_id', models.CharField(blank=True, max_length=20, null=True)),
                ('instagram_id', models.CharField(blank=True, max_length=20, null=True)),
                ('linkedin_likes', models.IntegerField(blank=True, null=True)),
                ('telegram_id', models.CharField(blank=True, max_length=20, null=True)),
                ('telegram_likes', models.IntegerField(blank=True, null=True)),
                ('tweet', models.CharField(blank=True, max_length=20, null=True)),
                ('twitter_likes', models.IntegerField(blank=True, null=True)),
                ('facebook_id', models.CharField(blank=True, max_length=20, null=True)),
                ('facebook_likes', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('favorite_count', models.IntegerField()),
                ('twitter_id', models.IntegerField()),
                ('id_str', models.CharField(max_length=30)),
                ('retweet_count', models.IntegerField()),
                ('text', models.TextField(max_length=280)),
            ],
        ),
        migrations.AlterField(
            model_name='linkedinpost',
            name='linkedin_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]