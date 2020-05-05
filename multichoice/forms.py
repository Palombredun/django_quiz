from django import forms
from django.forms import formset_factory

from multichoice.models import MCQuestion
from quiz.forms import QuestionForm


class MultiChoiceForm(QuestionForm):
	answer1 = forms.CharField(max_length=1000)
	answer1_correct = forms.BooleanField()
	answer2 = forms.CharField(max_length=1000)
	answer2_correct = forms.BooleanField()
	answer3 = forms.CharField(max_length=1000)
	answer3_correct = forms.BooleanField()

MC_Formset = formset_factory(MultiChoiceForm)