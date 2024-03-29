# Generated by Django 4.1 on 2022-08-28 10:19
from __future__ import annotations

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("socialmedia", "0013_regularsocialpost_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BackgroundImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="socialposts/backgrounds/"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="regularsocialpost",
            name="image_text",
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="regularsocialpost",
            name="share_image",
            field=models.BooleanField(default=False, verbose_name="Share image"),
        ),
        migrations.AddField(
            model_name="scheduledsocialpost",
            name="image_text",
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="scheduledsocialpost",
            name="share_image",
            field=models.BooleanField(default=False, verbose_name="Share image"),
        ),
        migrations.AlterField(
            model_name="regularsocialpost",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="socialposts/images/"
            ),
        ),
        migrations.AlterField(
            model_name="scheduledsocialpost",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="socialposts/images/"
            ),
        ),
        migrations.AddField(
            model_name="regularsocialpost",
            name="image_background",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="socialmedia.backgroundimage",
            ),
        ),
        migrations.AddField(
            model_name="scheduledsocialpost",
            name="image_background",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="socialmedia.backgroundimage",
            ),
        ),
    ]
