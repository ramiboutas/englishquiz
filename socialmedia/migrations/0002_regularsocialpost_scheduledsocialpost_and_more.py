# Generated by Django 4.0.5 on 2022-07-16 19:13
from __future__ import annotations

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("socialmedia", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="linkedinpost",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
