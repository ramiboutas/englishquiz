# Generated by Django 4.1 on 2022-08-15 10:26

from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0003_deepllanguage_formality"),
    ]

    operations = [
        migrations.CreateModel(
            name="TranslatedQuestion",
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
                ("original_text", models.CharField(max_length=650)),
                ("translated_text", models.CharField(max_length=650)),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quiz.deepllanguage",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.question"
                    ),
                ),
            ],
        ),
    ]
