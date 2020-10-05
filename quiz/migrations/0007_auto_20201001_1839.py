# Generated by Django 3.0.2 on 2020-10-01 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0006_detail_result'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Catégorie', 'verbose_name_plural': 'Catégories'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': 'Quiz'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Sous-catégorie', 'verbose_name_plural': 'Sous-catégories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(blank=True, help_text='Explication à afficher après que la question aient été répondue.', max_length=2000, null=True, verbose_name='Explication'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Category', verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True, help_text='une description du quiz', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.SubCategory', verbose_name='Sous-catégorie'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='url',
            field=models.SlugField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Category', verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Sous-Catégorie'),
        ),
    ]