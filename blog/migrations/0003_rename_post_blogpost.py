# Generated by Django 4.0.5 on 2022-08-09 21:55
from __future__ import annotations

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        ("blog", "0002_remove_post_unsplashid_alter_post_slug_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Post",
            new_name="BlogPost",
        ),
    ]
