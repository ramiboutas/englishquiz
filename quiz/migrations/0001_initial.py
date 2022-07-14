# Generated by Django 4.0.5 on 2022-07-14 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('level', models.IntegerField(choices=[(1, 'A1'), (2, 'A2'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2')], default=5)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('image_credits_url', models.URLField(null=True)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-views',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_one', models.CharField(blank=True, max_length=200, null=True)),
                ('text_two', models.CharField(blank=True, max_length=200, null=True)),
                ('text_three', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, '1: One text input'), (2, '2: Two text input'), (5, '5: One choice selection'), (6, '6: Multiple choice selection')], default=1)),
                ('explanation', models.CharField(blank=True, max_length=250, null=True)),
                ('promoted', models.BooleanField(default=False, editable=False)),
                ('lection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.lection')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='lection',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
        ),
    ]
