# Generated by Django 4.1 on 2022-08-28 10:23

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0014_backgroundimage_regularsocialpost_image_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="backgroundimage",
            name="name",
            field=models.CharField(max_length=20, null=True),
        ),
    ]