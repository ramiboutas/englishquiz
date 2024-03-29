# Generated by Django 4.0.8 on 2022-11-04 23:09
from __future__ import annotations

import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("socialmedia", "0021_delete_socialmediaposteditem_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="regularsocialpost",
            name="created_by",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="scheduledsocialpost",
            name="created_by",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
