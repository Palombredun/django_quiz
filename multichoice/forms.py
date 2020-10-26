from django import forms

from multichoice.models import MCQuestion
from quiz.forms import QuestionForm


class CreationMultiChoiceForm(QuestionForm):
    """
    Form dedicated to the creation of a MultiChoice Question.
    """
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
    """
    Form used for the taking of a quiz.
    It is used for getting the student's answer to  a multichoice question.
    This answer will be compared to the one decided by the creator of
    the quiz in order to decided if it is right or wrong.
    """
    answer1_correct = forms.BooleanField(required=False)
    answer2_correct = forms.BooleanField(required=False)
    answer3_correct = forms.BooleanField(required=False)
    id_question = forms.IntegerField(widget=forms.HiddenInput())