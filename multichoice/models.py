from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from quiz.models import Question


class MCQuestion(Question):

    answer1 = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))
    answer1_correct = models.BooleanField(blank=False, default=False)

    answer2 = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))
    answer2_correct = models.BooleanField(blank=False, default=False)

    answer3 = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))
    answer3_correct = models.BooleanField(blank=False, default=False)

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")