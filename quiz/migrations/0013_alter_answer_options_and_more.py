# Generated by Django 4.0.8 on 2022-11-05 01:05
from __future__ import annotations

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0012_remove_question_created_by"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"base_manager_name": "prefetch_manager"},
        ),
        migrations.AlterModelOptions(
            name="translatedquestion",
            options={"base_manager_name": "prefetch_manager"},
        ),
        migrations.AlterModelManagers(
            name="answer",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="lection",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="question",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="translatedquestion",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.question"
            ),
        ),
        migrations.AlterField(
            model_name="lection",
            name="quiz",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.quiz"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="lection",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.lection"
            ),
        ),
        migrations.AlterField(
            model_name="translatedquestion",
            name="language",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.deepllanguage"
            ),
        ),
        migrations.AlterField(
            model_name="translatedquestion",
            name="question",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.question"
            ),
        ),
    ]
