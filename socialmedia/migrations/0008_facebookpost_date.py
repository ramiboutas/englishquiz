# Generated by Django 4.0.5 on 2022-07-17 15:15
from __future__ import annotations

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("socialmedia", "0007_rename_post_id_facebookpost_facebook_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="facebookpost",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
