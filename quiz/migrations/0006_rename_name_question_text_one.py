# Generated by Django 4.0.3 on 2022-04-27 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_quiz_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='name',
            new_name='text_one',
        ),
    ]