# Generated by Django 4.2 on 2023-04-20 20:04
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0016_alter_question_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lection",
            options={"base_manager_name": "prefetch_manager", "ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"base_manager_name": "prefetch_manager", "ordering": ("id",)},
        ),
    ]
