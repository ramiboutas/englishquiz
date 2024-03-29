# Generated by Django 4.1 on 2022-08-18 05:37
from __future__ import annotations

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0010_blogpost_promoted"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="pdf",
            field=models.FileField(
                blank=True, null=True, upload_to="blog-posts/%Y/%m/%d"
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
