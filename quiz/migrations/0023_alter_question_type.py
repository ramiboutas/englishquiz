# Generated by Django 4.2.4 on 2024-01-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0022_alter_question_explanation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, '1: One text input'), (2, '2: Two text inputs'), (5, '5: One choice selection')], default=5),
        ),
    ]
