# Generated by Django 4.1 on 2022-08-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_remove_deepllanguage_formality_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='translatedquestion',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='translatedquestion',
            name='updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]