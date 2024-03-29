# Generated by Django 4.0.5 on 2022-07-16 19:22
from __future__ import annotations

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("socialmedia", "0002_regularsocialpost_scheduledsocialpost_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="regularsocialpost",
            name="image_text",
        ),
        migrations.RemoveField(
            model_name="scheduledsocialpost",
            name="image_text",
        ),
        migrations.AddField(
            model_name="regularsocialpost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="socialposts/"),
        ),
        migrations.AddField(
            model_name="scheduledsocialpost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="socialposts/"),
        ),
    ]
