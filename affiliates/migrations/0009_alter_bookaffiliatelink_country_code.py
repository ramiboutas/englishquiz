# Generated by Django 4.0.9 on 2023-02-04 21:31
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("affiliates", "0008_countryvisitor_alter_bookaffiliatelink_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookaffiliatelink",
            name="country_code",
            field=models.CharField(
                choices=[
                    ("US", "USA"),
                    ("DE", "Germany"),
                    ("ES", "Spain"),
                    ("IT", "Italy"),
                    ("FR", "France"),
                    ("UK", "United Kingdom"),
                ],
                max_length=2,
            ),
        ),
    ]
