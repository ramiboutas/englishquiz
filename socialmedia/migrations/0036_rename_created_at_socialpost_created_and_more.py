# Generated by Django 4.2.4 on 2023-10-03 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0035_socialpost_promote_in_facebook_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialpost',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='socialpost',
            old_name='updated_at',
            new_name='updated',
        ),
    ]
