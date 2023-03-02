# Generated by Django 4.1.3 on 2023-03-02 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0002_alter_questions_options_alter_quizzes_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
    ]
