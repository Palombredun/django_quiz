from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from quiz.models import Question


class TF_Question(Question):
    correct = models.BooleanField(
        blank=False,
        default=False,
        help_text=_(
            "Tick this if the question " "is true. Leave it blank for" " false."
        ),
        verbose_name=_("Correct"),
    )

    class Meta:
        verbose_name = _("True/False Question")
        verbose_name_plural = _("True/False Questions")
