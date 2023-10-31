# Generated by Django 4.2.4 on 2023-10-30 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0016_bookaffiliatelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(null=True, upload_to='books'),
        ),
        migrations.AddField(
            model_name='book',
            name='promoted',
            field=models.BooleanField(default=False),
        ),
    ]