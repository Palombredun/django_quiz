from django import forms
from django.forms import formset_factory

from quiz.forms import QuestionForm
from .models import TF_Question

CORRECTNESS_CHOICES = ((True, "Vrai"), (False, "Faux"))


class TrueFalseForm(QuestionForm):
    correct = forms.ChoiceField(choices=CORRECTNESS_CHOICES, label="Réponse")


TF_Formset = formset_factory(TrueFalseForm)
