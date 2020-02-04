from __future__ import unicode_literals
import re
import json

from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.conf import settings

from model_utils.managers import InheritanceManager



class Category(models.Model):

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category


class SubCategory(models.Model):

    sub_category = models.CharField(
        verbose_name=_("Sub-Category"),
        max_length=250, blank=True, null=True)

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=_("Category"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Sub-Category")
        verbose_name_plural = _("Sub-Categories")

    def __str__(self):
        return self.sub_category + " (" + self.category.category + ")"


class Quiz(models.Model):

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the quiz"))

    url = models.SlugField(
        max_length=16, blank=False, unique=True,
        help_text=_("a user friendly url"),
        verbose_name=_("user friendly url"))

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=_("Category"), on_delete=models.CASCADE)
    
    # new
    subcategory = models.ForeignKey(
        SubCategory, null=True, blank=True,
        verbose_name=_("Subcategory"), on_delete=models.CASCADE)

    # new
    date = models.DateTimeField(
        auto_now=True)

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in "
                    "a random order or as they "
                    "are set?"))

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)

    # new
    difficulty = models.IntegerField(default=2, blank=False, null=False)

    # new
    order = models.BooleanField(default=True,
                                help_text=_("Ordre des questions : aléatoire ou "
                                "dans l'ordre de création des questions."
                                ))

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name=_("Figure"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Entrez la question à poser"),
                               verbose_name=_('Question'))

    explanation = models.TextField(max_length=2000,
                                   blank=True,
                                   null=True,
                                   help_text=_("Explanation to be shown "
                                               "after the question has "
                                               "been answered."),
                                   verbose_name=_('Explanation'))

    theme1 = models.CharField(max_length=50,
                                blank=True, null=True,
                                help_text=_("Thème de la question. Plus précis que "
                                            "la sous-catégorie, il permettra de "
                                            "rédiger les conseils en fin de quiz."
                                ))

    theme2 = models.CharField(max_length=50,
                                blank=True, null=True,
                                help_text=_("Thème de la question. Plus précis que "
                                            "la sous-catégorie, il permettra de "
                                            "rédiger les conseils en fin de quiz."
                                ))

    theme3 = models.CharField(max_length=50,
                                blank=True, null=True,
                                help_text=_("Thème de la question. Plus précis que "
                                            "la sous-catégorie, il permettra de "
                                            "rédiger les conseils en fin de quiz."
                                ))

    
    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        #ordering = ['category']

    def __str__(self):
        return self.content