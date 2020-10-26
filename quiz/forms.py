from django import forms

from quiz.models import Quiz, Question, Category, SubCategory


DIFFICULTY_CHOICES = ((1, "facile"), (2, "moyen"), (3, "difficile"))



class QuestionForm(forms.Form):
    """
    Base form used for the creation of questions in a quiz.
    """

    content = forms.CharField(max_length=1000, label="Question")
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, label="Difficulté")
    theme1 = forms.CharField(
        max_length=100,
        label="Thème 1",
        help_text="Thème de la question",
        required=False,
    )
    theme2 = forms.CharField(
        max_length=100,
        label="Thème 2",
        help_text="Thème de la question",
        required=False,
    )
    theme3 = forms.CharField(
        max_length=100,
        label="Thème 3",
        help_text="Thème de la question",
        required=False,
    )
    order = forms.IntegerField(widget=forms.HiddenInput())


class QuizForm(forms.ModelForm):
    """
    Form used for the creation of a quiz. 
    """
    
    class Meta:
        model = Quiz
        fields = ("title", "description", "category", "sub_category", "random_order")
        labels = {
            "title": "Titre",
            "category": "Catégorie",
            "sub_category": "Sous-catégorie",
            "random_order": "Ordre aléatoire",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sub_category"].queryset = SubCategory.objects.none()
