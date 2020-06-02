from django import forms
from django.forms import formset_factory

from multichoice.models import MCQuestion
from quiz.forms import QuestionForm


class MultiChoiceForm(QuestionForm):
    answer1 = forms.CharField(max_length=1000)
    answer1_correct = forms.BooleanField(required=False)
    answer2 = forms.CharField(max_length=1000)
    answer2_correct = forms.BooleanField(required=False)
    answer3 = forms.CharField(max_length=1000)
    answer3_correct = forms.BooleanField(required=False)


MC_Formset = formset_factory(MultiChoiceForm)
