from django import forms
from django.forms import formset_factory

from quiz.forms import QuestionForm
from .models import TF_Question

class TrueFalseForm(QuestionForm):
	correct = forms.BooleanField()

TF_Formset = formset_factory(TrueFalseForm)