# Generated by Django 4.0.5 on 2022-08-10 21:38
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_remove_blogpost_status_blogpost_public"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpost",
            old_name="author",
            new_name="created_by",
        ),
    ]
