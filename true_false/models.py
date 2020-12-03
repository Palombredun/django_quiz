from django.db import models

from quiz.models import Question


class TF_Question(Question):
    """
    Model used for the creation whose answer it is either right or wrong.
    """

    correct = models.BooleanField(blank=False, default=False)

    class Meta:
        verbose_name = "Question Vrai/Faux"
        verbose_name_plural = "Questions Vrai/Faux"
