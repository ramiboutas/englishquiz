# Generated by Django 4.1 on 2022-08-28 11:19
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "socialmedia",
            "0018_rename_image_background_regularsocialpost_background_image_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="regularsocialpost",
            old_name="background_image",
            new_name="background_image_obj",
        ),
        migrations.RenameField(
            model_name="scheduledsocialpost",
            old_name="background_image",
            new_name="background_image_obj",
        ),
    ]
