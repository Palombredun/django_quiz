from django.db import models

from quiz.models import Question


class MCQuestion(Question):
    """
    Modele utilisé pour la création d'une question dont la réponse
    contient 3 choix. Au moins l'un d'eux doit être correct. 
    Model used for the creation of a question which contains 3 propositions.
    At least 1 of these propositions must be checked to be correct, up to the
    three.
    """
    answer1 = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name="Content",
    )
    answer1_correct = models.BooleanField(blank=False, default=False)

    answer2 = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name="Content",
    )
    answer2_correct = models.BooleanField(blank=False, default=False)

    answer3 = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name="Content",
    )
    answer3_correct = models.BooleanField(blank=False, default=False)

    class Meta:
        verbose_name = "Question à choix multiples"
        verbose_name_plural = "Questions à choix multiples"
