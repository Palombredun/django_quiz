from django import forms

from quiz.models import Quiz, Question, Category, SubCategory


DIFFICULTY_CHOICES = ((1, "facile"), (2, "moyen"), (3, "difficile"))


class QuestionForm(forms.Form):
    content = forms.CharField(max_length=1000, label="Question")
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, label="Difficulté")
    theme = forms.CharField(
        max_length=100, label="Thème", help_text="thème de la question"
    )
    order = forms.IntegerField(widget=forms.HiddenInput())

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("title", "description", "category", "sub_category", "random_order")
        labels ={
        	"title": "titre",
        	"category": "catégorie",
        	"sub_category": "sous-catégorie",
        	"random_order": "ordre aléatoire"
        }