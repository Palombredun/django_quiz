from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown


class Category(models.Model):

    category = models.CharField(
        verbose_name="Catégorie", max_length=250, blank=True, unique=True, null=True
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.category


class SubCategory(models.Model):

    sub_category = models.CharField(
        verbose_name="Sous-Catégorie", max_length=250, blank=True, null=True
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Catégorie",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"

    def __str__(self):
        return self.sub_category + " (" + self.category.category + ")"


class Quiz(models.Model):

    title = models.CharField(verbose_name="Titre", max_length=60, blank=False)

    description = models.TextField(
        verbose_name="Description", blank=True, help_text="une description du quiz"
    )

    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    url = models.SlugField(max_length=16, blank=False, unique=True, db_index=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        verbose_name="Catégorie",
        on_delete=models.CASCADE,
    )

    sub_category = models.ForeignKey(
        SubCategory,
        null=True,
        blank=True,
        verbose_name="Sous-catégorie",
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(auto_now=True)

    random_order = models.BooleanField(
        blank=False,
        default=False,
        verbose_name="Ordre aléatoire",
        help_text="Afficher les questions dans l'ordre de création ou aléatoirement ?",
    )

    difficulty = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ForeignKey(
        Quiz, verbose_name="Quiz", default=1, on_delete=models.CASCADE
    )
    difficulty = models.IntegerField(default=2, blank=False, null=False)
    order = models.IntegerField(null=True)
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
        help_text="Explication à afficher "
        "après que la question "
        "aient été répondue.",
        verbose_name="Explication",
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

    def get_question_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode="escape"))
        # {{ question.content }}
        # >
        # {{ question.get_question_as_markdown }}

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        # ordering = ['category']

    def __str__(self):
        return self.content


class AnswerUser(models.Model):
    user = models.ManyToManyField(User)
    question = models.ManyToManyField(Question)
    correct = models.BooleanField()


class Result(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    student = models.ManyToManyField(User)
    easy = models.FloatField()
    medium = models.FloatField()
    difficult = models.FloatField()
    theme1 = models.FloatField()
    theme2 = models.FloatField()
    theme3 = models.FloatField()
    result_0_to_3 = models.FloatField()
    result_4_to_6 = models.FloatField()
    result_7_to_10 = models.FloatField()
