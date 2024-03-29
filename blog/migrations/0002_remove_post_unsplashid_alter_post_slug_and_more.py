# Generated by Django 4.0.5 on 2022-08-09 21:53
from __future__ import annotations

import slugger.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="unsplashID",
        ),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=slugger.fields.AutoSlugField(populate_from="title"),
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "DRAFT"), (1, "PUBLISH")], default=0
            ),
        ),
    ]
