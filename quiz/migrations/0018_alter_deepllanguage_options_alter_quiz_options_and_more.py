# Generated by Django 4.2.4 on 2023-11-07 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_alter_lection_options_alter_question_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deepllanguage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={},
        ),
        migrations.RemoveField(
            model_name='deepllanguage',
            name='views',
        ),
        migrations.RemoveField(
            model_name='lection',
            name='views',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='views',
        ),
    ]
