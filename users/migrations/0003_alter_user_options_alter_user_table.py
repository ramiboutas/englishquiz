# Generated by Django 4.0.8 on 2022-11-04 19:51
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_rename_user_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AlterModelTable(
            name="user",
            table="auth_user",
        ),
    ]
