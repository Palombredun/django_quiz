from django import forms

from quiz.models import Question


DIFFICULTY_CHOICES = (
    (1, 'facile'),
    (2, 'moyen'),
    (3, 'difficile')
    )

class QuestionForm(forms.Form):
	difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES)
	order = forms.BooleanField()
	content = forms.CharField(max_length=1000)
	