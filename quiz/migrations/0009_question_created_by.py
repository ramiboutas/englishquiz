# Generated by Django 4.0.8 on 2022-11-03 20:35
from __future__ import annotations

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quiz", "0008_alter_deepllanguage_options_deepllanguage_views"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
