# Generated by Django 3.1.2 on 2020-11-20 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiz_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_participants', models.IntegerField()),
                ('mean', models.IntegerField()),
                ('easy', models.IntegerField()),
                ('medium', models.IntegerField()),
                ('difficult', models.IntegerField()),
                ('quiz', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('statistics', models.ManyToManyField(to='quiz.Statistic')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('statistics', models.ManyToManyField(to='quiz.Statistic')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('score', models.IntegerField()),
                ('statistics', models.ManyToManyField(to='quiz.Statistic')),
            ],
        ),
    ]
