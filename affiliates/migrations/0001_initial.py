# Generated by Django 4.0.8 on 2023-01-31 17:33
import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("name", models.CharField(max_length=64)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("a1", "A1"),
                            ("a2", "A2"),
                            ("b1", "B1"),
                            ("b2", "B2"),
                            ("c1", "C1"),
                            ("c2", "C2"),
                        ],
                        default="b2",
                        max_length=2,
                    ),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("featured", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="BookAffiliateLink",
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
                ("url", models.URLField()),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("global", "Global"),
                            ("US", "USA"),
                            ("DE", "Germany"),
                            ("ES", "Spain"),
                            ("FR", "France"),
                            ("IT", "Italy"),
                        ],
                        max_length=6,
                    ),
                ),
                (
                    "book",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="affiliates.book",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
