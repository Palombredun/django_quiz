# Generated by Django 3.0.2 on 2020-02-04 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, null=True, to='quiz.Quiz', verbose_name='Quiz'),
        ),
    ]