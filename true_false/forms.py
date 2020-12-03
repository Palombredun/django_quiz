from django import forms
from django.forms import formset_factory

from quiz.forms import QuestionForm
from .models import TF_Question


TRUE_FALSE_CHOICES = ((None, ""), (True, "Vrai"), (False, "Faux"))


class CreationTrueFalseForm(QuestionForm):
    """
    Form dedicated to the creation of a TrueFalse Question.
    """

    correct = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        label="Réponse",
        widget=forms.Select(),
        required=True,
    )

    class Meta:
        model = TF_Question
        fields = ("content", "difficulty", "order", "theme1", "theme2", "theme3")


class TrueFalseForm(forms.Form):
    """
    Form used for the taking of a quiz.
    It is used for the getting the student's answer to a true/false question.
    This answer will be compared to the one chosen by the creator of the
    quiz to determine if it is correct.
    """

    correct = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES, widget=forms.Select(), required=True
    )
    qid = forms.IntegerField(widget=forms.HiddenInput())
