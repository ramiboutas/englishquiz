# Generated by Django 4.1 on 2022-08-21 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_contact_responded_contact_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='subscribe',
            field=models.BooleanField(default=False, verbose_name='Subscribe to our Newsletter'),
        ),
    ]
