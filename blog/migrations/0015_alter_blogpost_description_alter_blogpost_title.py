# Generated by Django 4.1 on 2022-08-28 10:19

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_remove_blogpost_recreate_pdf"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(max_length=70),
        ),
    ]
