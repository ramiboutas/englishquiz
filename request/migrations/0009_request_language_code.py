# Generated by Django 4.2 on 2023-06-15 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0008_alter_request_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='language_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='language code'),
        ),
    ]