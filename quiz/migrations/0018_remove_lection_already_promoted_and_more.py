# Generated by Django 4.0.5 on 2022-06-25 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_lection_already_promoted_quiz_already_promoted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lection',
            name='already_promoted',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='already_promoted',
        ),
    ]