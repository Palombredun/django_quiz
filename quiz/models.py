from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    category = models.CharField(
        verbose_name="Category", max_length=250, blank=True, unique=True, null=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class SubCategory(models.Model):

    sub_category = models.CharField(
        verbose_name="Sub-Category", max_length=250, blank=True, null=True
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Category",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Categories"

    def __str__(self):
        return self.sub_category + " (" + self.category.category + ")"


class Quiz(models.Model):

    title = models.CharField(verbose_name="Title", max_length=60, blank=False)

    description = models.TextField(
        verbose_name="Description", blank=True, help_text="a description of the quiz"
    )

    creator = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    url = models.SlugField(
        max_length=16,
        blank=False,
        unique=True,
        help_text="a user friendly url",
        verbose_name="user friendly url",
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Category",
        on_delete=models.CASCADE,
    )

    sub_category = models.ForeignKey(
        SubCategory,
        null=True,
        blank=True,
        verbose_name="Subcategory",
        on_delete=models.CASCADE,
    )

    date = models.DateTimeField(auto_now=True)

    random_order = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Ordre aléatoire",
        help_text="Afficher les questions dans l'ordre de création ou aléatoirement ?",
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ManyToManyField(Quiz, verbose_name="Quiz", blank=True)

    # new
    difficulty = models.IntegerField(default=2, blank=False, null=False)

    # new
    order = models.IntegerField(null=True)

    ordered = models.BooleanField(
        default=True,
        help_text="Ordre des questions : aléatoire ou "
        "dans l'ordre de création des questions.",
    )

    figure = models.ImageField(
        upload_to="uploads/%Y/%m/%d", blank=True, null=True, verbose_name="Figure"
    )

    content = models.CharField(
        max_length=1000,
        blank=False,
        help_text="Entrez la question à poser",
        verbose_name="Question",
    )

    explanation = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        help_text="Explanation to be shown " "after the question has " "been answered.",
        verbose_name="Explanation",
    )

    theme1 = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=(
            "Thème de la question. Plus précis que "
            "la sous-catégorie, il permettra de "
            "rédiger les conseils en fin de quiz."
        ),
    )

    theme2 = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Thème de la question. Plus précis que "
        "la sous-catégorie, il permettra de "
        "rédiger les conseils en fin de quiz.",
    )

    theme3 = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Thème de la question. Plus précis que "
        "la sous-catégorie, il permettra de "
        "rédiger les conseils en fin de quiz.",
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        # ordering = ['category']

    def __str__(self):
        return self.content
