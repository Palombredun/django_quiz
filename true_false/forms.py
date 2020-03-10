from django import forms

from quiz.forms import QuestionForm
from .models import TF_Question

class TrueFalseForm(QuestionForm):
	correct = forms.BooleanField()