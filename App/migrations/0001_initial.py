# Generated by Django 4.1.3 on 2023-03-01 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True, verbose_name='Category Name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True, verbose_name='Quiz title')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App.category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advance'), (4, 'Expert')], default=1, verbose_name='Difficulty')),
                ('question', models.CharField(max_length=1000, unique=True, verbose_name='Question')),
                ('option_one', models.CharField(max_length=250, verbose_name='Option 1')),
                ('option_two', models.CharField(max_length=250, verbose_name='Option 2')),
                ('option_three', models.CharField(blank=True, max_length=250, verbose_name='Option 3')),
                ('correct_answer', models.CharField(max_length=250)),
                ('availible', models.BooleanField(default=True, verbose_name='Availible')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Created at')),
                ('date_updated', models.DateField(auto_now=True, verbose_name='Updated at')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App.quizzes', verbose_name='Quiz Title')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.CharField(max_length=250)),
                ('score', models.IntegerField(default=0, verbose_name='Current Score')),
                ('available', models.IntegerField(default=0)),
                ('average', models.FloatField(default=0)),
                ('attempts', models.IntegerField(default=1)),
                ('percentage', models.FloatField(default=0)),
                ('date_played', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App.questions')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App.quizzes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
