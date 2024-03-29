# Generated by Django 4.0.5 on 2022-08-09 21:14
from __future__ import annotations

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations
from django.db import models

import markdownx.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(max_length=250)),
                ("content", markdownx.models.MarkdownxField()),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "DRAFT"), (1, "PUBLISHED")], default=0
                    ),
                ),
                ("unsplashID", models.CharField(blank=True, max_length=40)),
                (
                    "level",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "BEGINNER"), (2, "INTERMEDIATE"), (3, "ADVANCED")],
                        default=1,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
    ]
