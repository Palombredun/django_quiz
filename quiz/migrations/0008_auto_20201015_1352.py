# Generated by Django 3.0.2 on 2020-10-15 13:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0007_auto_20201001_1839'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Detail',
            new_name='AnswerUser',
        ),
    ]
