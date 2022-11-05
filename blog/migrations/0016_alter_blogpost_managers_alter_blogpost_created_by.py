# Generated by Django 4.0.8 on 2022-11-05 01:05

import auto_prefetch
from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_alter_blogpost_description_alter_blogpost_title'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blogpost',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('prefetch_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='created_by',
            field=auto_prefetch.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
