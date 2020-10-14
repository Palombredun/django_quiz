from django import forms
from django.forms import formset_factory

from multichoice.models import MCQuestion
from quiz.forms import QuestionForm


class CreationMultiChoiceForm(QuestionForm):
    answer1 = forms.CharField(max_length=1000, label="Réponse 1")
    answer1_correct = forms.BooleanField(required=False, label="Correcte")
    answer2 = forms.CharField(max_length=1000, label="Réponse 2")
    answer2_correct = forms.BooleanField(required=False, label="Correcte")
    answer3 = forms.CharField(max_length=1000, label="Réponse 3")
    answer3_correct = forms.BooleanField(required=False, label="Correcte")

    class Meta:
        model = MCQuestion
        fields = (
            "content",
            "difficulty",
            "order",
            "theme1",
            "theme2",
            "theme3",
            "answer1",
            "answer1_correct",
            "answer2",
            "answer2_correct",
            "answer3",
            "answer3_correct",
        )


class MultiChoiceForm(forms.Form):
    answer1 = forms.CharField(max_length=1000)
    answer1_correct = forms.BooleanField(required=False)
    answer2 = forms.CharField(max_length=1000)
    answer2_correct = forms.BooleanField(required=False)
    answer3 = forms.CharField(max_length=1000)
    answer3_correct = forms.BooleanField(required=False)

    class Meta:
        model = MCQuestion
        field = (
            "answer1",
            "answer1_correct",
            "answer2",
            "answer2_correct",
            "answer3",
            "answer3_correct",
        )
