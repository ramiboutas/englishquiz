# Generated by Django 4.2 on 2023-08-29 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_remove_blogpost_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='level',
        ),
    ]
