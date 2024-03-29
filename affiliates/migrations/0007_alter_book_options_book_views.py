# Generated by Django 4.0.8 on 2023-02-04 11:12
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("affiliates", "0006_alter_book_category_alter_book_test_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ("-views",)},
        ),
        migrations.AddField(
            model_name="book",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
