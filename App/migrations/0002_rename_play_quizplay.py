# Generated by Django 4.1.3 on 2023-03-02 17:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Play',
            new_name='QuizPlay',
        ),
    ]
