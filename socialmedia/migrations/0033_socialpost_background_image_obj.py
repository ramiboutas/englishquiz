# Generated by Django 4.2.4 on 2023-10-03 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0032_socialpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialpost',
            name='background_image_obj',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='socialmedia.backgroundimage'),
        ),
    ]