# Generated by Django 4.0.8 on 2023-01-09 06:09
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("socialmedia", "0025_alter_regularsocialpost_background_image_obj_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoriteTweetSearch",
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
                ("name", models.CharField(max_length=50)),
                ("lang_code", models.CharField(max_length=2)),
                ("number_of_likes", models.PositiveSmallIntegerField(default=5)),
            ],
        ),
    ]
