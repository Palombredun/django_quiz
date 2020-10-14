from django import forms
from django.forms import formset_factory

from quiz.forms import QuestionForm
from .models import TF_Question

CORRECTNESS_CHOICES = ((True, "Vrai"), (False, "Faux"))


class CreationTrueFalseForm(QuestionForm):
    correct = forms.ChoiceField(choices=CORRECTNESS_CHOICES, label="Réponse")

    class Meta:
        model = TF_Question
        fields = ("content", "difficulty", "order", "theme1", "theme2", "theme3")


class TrueFalseForm(forms.Form):
    correct = forms.ChoiceField(choices=CORRECTNESS_CHOICES)

    class Meta:
        model = TF_Question
        fields = ("content", "correct")
